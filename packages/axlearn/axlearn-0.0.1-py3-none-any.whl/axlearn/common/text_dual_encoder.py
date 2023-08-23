# Copyright © 2023 Apple Inc.

"""Text-based dual-encoder module."""

from typing import Dict, Optional, Tuple

import jax.numpy as jnp

from axlearn.common.base_layer import BaseLayer
from axlearn.common.config import REQUIRED, Required, config_class
from axlearn.common.layers import Linear
from axlearn.common.loss import (
    asymmetric_contrastive_loss_from_logits,
    contrastive_logits,
    ranking_pairwise_loss,
)
from axlearn.common.module import Module, child_context
from axlearn.common.multi_stream_model import FusionNetwork, MultiStreamModel, StreamEncoder
from axlearn.common.text_encoder import TEXT_EMBEDDINGS, TextEmbeddingEncoder
from axlearn.common.utils import NestedTensor, Tensor

POSITIVE_EMBEDDINGS = "positive_embeddings"
NEGATIVE_EMBEDDINGS = "negative_embeddings"
POSITIVE_PADDINGS = "positive_paddings"
NEGATIVE_PADDINGS = "negative_paddings"
POSITIVE_INPUT_IDS = "positive_input_ids"
NEGATIVE_INPUT_IDS = "negative_input_ids"
RIGHT_PADDINGS = "right_paddings"

FLATTENED_LEFT_EMBEDDINGS = "flattened_left_embeddings"
FLATTENED_RIGHT_EMBEDDINGS = "flattened_right_embeddings"

SIMILARITY_MATRIX = "similarity_matrix"

PAIRWISE_LOSS_INPUT_IDS = "pairwise_loss_input_ids"
PAIRWISE_LOSS_PADDINGS = "pairwise_loss_paddings"
PAIRWISE_LOSS_EMBEDDINGS = "pairwise_loss_embeddings"
RANKS = "ranks"

NUM_VALID_RANKING_PAIRS = "num_valid_ranking_pairs"

ENCODING_FIELD_MAP = {
    POSITIVE_EMBEDDINGS: POSITIVE_INPUT_IDS,
    NEGATIVE_EMBEDDINGS: NEGATIVE_INPUT_IDS,
    PAIRWISE_LOSS_EMBEDDINGS: PAIRWISE_LOSS_INPUT_IDS,
}

TEXT_DUAL_ENCODER_SHARED_MODULE_NAME = "shared_text_encoder"


class TextEmbeddingStreamEncoder(StreamEncoder):
    """A StreamEncoder that encodes inputs with a configured TextEmbeddingEncoder and outputs
    embeddings optionally applied with a linear projection and/or a normalization layer.
    """

    @config_class
    class Config(StreamEncoder.Config):
        """Configures TextEmbeddingStreamEncoder."""

        # Output dimension from this TextEmbeddingStreamEncoder.
        output_dim: Required[int] = REQUIRED
        # A map having output embedding name as key and input id name as value. All specified input
        # ids will be encoded by text_encoder and stored in input_batch with output embedding name
        # as the field name.
        encoding_field_map: Dict[str, str] = ENCODING_FIELD_MAP
        # Text encoder that outputs a single embedding vector for each input sequence.
        text_encoder: TextEmbeddingEncoder.Config = TextEmbeddingEncoder.default_config()
        # Hidden dimension of base text_encoder. If None, it is assumed to be the same as
        # output_dim.
        hidden_dim: Optional[int] = None
        # Optional linear projection layer applied on embedding from text_encoder. If None,
        # embedding from text_encoder is taken as it is.
        output_proj: Optional[Linear.Config] = None
        # Optional normalization layer applied on embedding from text_encoder and after potential
        # projection layer. If None, no normalization will be applied.
        output_norm: Optional[BaseLayer.Config] = None

    def __init__(self, cfg: Config, *, parent: Module):
        super().__init__(cfg, parent=parent)
        cfg = self.config

        if cfg.hidden_dim is not None:
            hidden_dim = cfg.hidden_dim
        else:
            hidden_dim = cfg.output_dim

        self._add_child("text_encoder", cfg.text_encoder.set(output_dim=hidden_dim))

        if hidden_dim != cfg.output_dim:
            assert (
                cfg.output_proj is not None
            ), "output_proj can't be None when hidden_dim != output_dim."

        if cfg.output_proj is not None:
            self._add_child(
                "output_proj", cfg.output_proj.set(input_dim=hidden_dim, output_dim=cfg.output_dim)
            )
        if cfg.output_norm is not None:
            self._add_child("output_norm", cfg.output_norm)

    def forward(self, input_batch: NestedTensor) -> NestedTensor:
        """Forward function.

        Args:
            input_batch: A dictionary containing all values of cfg.encoding_field_map as keys.
                Each value of input_batch is a Tensor with shape
                [batch_size, num_inputs_per_example, max_seq_len].

        Returns:
            An updated input_batch dict where all keys of cfg.encoding_field_map are added. Each
            value of the new key is a Tensor with shape
            [batch_size, num_inputs_per_example, output_dim].
        """

        def encode(input_ids: Tensor) -> NestedTensor:
            embeddings = self.text_encoder(input_ids)[TEXT_EMBEDDINGS]
            if "output_proj" in self.children:
                embeddings = self.output_proj(embeddings)
            if "output_norm" in self.children:
                embeddings = self.output_norm(embeddings)
            return embeddings

        cfg = self.config

        for output_emb_field, input_id_field in cfg.encoding_field_map.items():
            if input_id_field in input_batch and input_batch[input_id_field].shape[1] > 0:
                input_ids = input_batch[input_id_field]
                batch_size, num_inputs_per_example, max_seq_len = input_ids.shape
                # Shape: [batch_size * num_inputs_per_example, max_seq_len].
                flattened_input_ids = input_ids.reshape(-1, max_seq_len)

                with child_context(f"encode_{input_id_field}", module=self):
                    embeddings = encode(flattened_input_ids)
                # Shape: [batch_size * num_inputs_per_example, output_dim].
                embeddings = embeddings.squeeze(axis=1)

                input_batch[output_emb_field] = embeddings.reshape(
                    batch_size, num_inputs_per_example, -1
                )

        return input_batch


def flatten_and_concat_embeddings(
    *,
    left_positive_embeddings: Tensor,
    right_positive_embeddings: Tensor,
    right_positive_paddings: Tensor,
    right_negative_embeddings: Optional[Tensor] = None,
    right_negative_paddings: Optional[Tensor] = None,
) -> Dict[str, Tensor]:
    """Flattens left and right embeddings and concatenates right encoder positive and negative
    embeddings.

    Args:
        left_positive_embeddings: A Tensor with shape [num_left_inputs, 1, dim].
        right_positive_embeddings: A Tensor with shape
            [num_left_inputs, max_right_positive_inputs, dim].
        right_positive_paddings: A 0/1 Tensor with shape
            [num_left_inputs, max_right_positive_inputs] where 1 means padded docs and 0 means
            effective docs.
        right_negative_embeddings: An optional Tensor with shape
            [num_left_inputs, max_right_negative_inputs, dim].
        right_negative_paddings: An optional 0/1 Tensor with shape
            [num_left_inputs, max_right_negative_inputs] where 1 means padded docs and
            0 means effective docs.

    Returns:
        A dict of Tensor:
            FLATTENED_LEFT_EMBEDDINGS: A Tensor with shape [num_left_inputs, dim].
            FLATTENED_RIGHT_EMBEDDINGS: A Tensor with shape
                [num_left_inputs * (max_right_positive_inputs + max_right_negative_inputs), dim].
                max_right_negative_inputs = 0 when there is no right_negative_embeddings.
            RIGHT_PADDINGS: A Tensor with shape
                [num_left_inputs * (max_right_positive_inputs + max_right_negative_inputs)].
                max_right_negative_inputs = 0 when there is no right_negative_embeddings.
    """
    embedding_dim = left_positive_embeddings.shape[-1]
    assert (
        left_positive_embeddings.shape[1] == 1
    ), "Expecting one positive embedding per example from left encoder."
    # Shape: [num_left_inputs, dim].
    flattened_left_embeddings = left_positive_embeddings.reshape(-1, embedding_dim)
    assert (
        right_positive_embeddings.shape[-1] == embedding_dim
    ), "right_positive_embeddings has a different dim than that of left_embeddings!"
    # Shape: [num_left_inputs * max_right_positive_inputs, dim].
    flattened_right_positive_embeddings = right_positive_embeddings.reshape(-1, embedding_dim)
    if right_negative_embeddings is not None:
        assert (
            right_negative_embeddings.shape[-1] == embedding_dim
        ), "right_negative_embeddings has a different dim than that of left_embeddings!"
        # Shape: [num_left_inputs * max_right_negative_inputs, dim].
        flattened_right_negative_embeddings = right_negative_embeddings.reshape(-1, embedding_dim)
        # Shape: [num_left_inputs * (max_right_positive_inputs + max_right_negative_inputs), dim].
        flattened_right_embeddings = jnp.concatenate(
            [flattened_right_positive_embeddings, flattened_right_negative_embeddings], axis=0
        )
        # Shape: [num_left_inputs * max_right_positive_inputs].
        flattened_right_positive_paddings = jnp.reshape(right_positive_paddings, -1)
        # Shape: [num_left_inputs * max_right_negative_inputs].
        flattened_right_negative_paddings = jnp.reshape(right_negative_paddings, -1)
        # Shape: [num_left_inputs * (max_right_positive_inputs + max_right_negative_inputs)].
        right_paddings = jnp.concatenate(
            [flattened_right_positive_paddings, flattened_right_negative_paddings]
        )
    else:
        # Shape: [num_left_inputs * max_right_positive_inputs, dim].
        flattened_right_embeddings = flattened_right_positive_embeddings
        # Shape: [num_left_inputs * max_right_positive_inputs].
        right_paddings = jnp.reshape(right_positive_paddings, -1)

    return {
        FLATTENED_LEFT_EMBEDDINGS: flattened_left_embeddings,
        FLATTENED_RIGHT_EMBEDDINGS: flattened_right_embeddings,
        RIGHT_PADDINGS: right_paddings,
    }


class TextEmbeddingAsymmetricContrastiveLossLayer(FusionNetwork):
    """A FusionNetwork that computes asymmetric contrastive loss using text embeddings from
    left and right encoders.

    Asymmetric contrastive loss means the softmax cross-entropy loss will only be
    calculated for each query among all candidate keys, but not vice versa.

    This loss layer expects left encoder contributing one embedding per example as queries. Right
    encoder contributes one positive embedding and optionally some number of negative embeddings per
    example as keys.
    """

    @config_class
    class Config(BaseLayer.Config):
        # Name of left encoder that gives embeddings as queries when computing asymmetric
        # contrastive loss.
        left_encoder_name: Required[str] = REQUIRED
        # Name of right encoder that gives embeddings as keys when computing asymmetric
        # contrastive loss.
        right_encoder_name: Required[str] = REQUIRED
        # A positive scalar float to be multiplied with logits. Default is 1.0.
        contrastive_loss_scale_factor: float = 1.0

    def _flatten_and_concat_embeddings(self, input_batch: NestedTensor) -> Dict[str, Tensor]:
        """Flattens left and right embeddings and concatenates right encoder positive and negative
        embeddings.
        """
        cfg = self.config
        left_encoder_name = cfg.left_encoder_name
        right_encoder_name = cfg.right_encoder_name

        right_positive_embeddings = input_batch[right_encoder_name][POSITIVE_EMBEDDINGS]
        assert (
            right_positive_embeddings.shape[1] == 1
        ), "Expecting one positive embedding per example from right encoder."

        right_positive_paddings = input_batch[right_encoder_name][POSITIVE_PADDINGS]
        assert (
            right_positive_paddings.shape[1] == 1
        ), "Expecting one positive embedding per example from right encoder."

        return flatten_and_concat_embeddings(
            left_positive_embeddings=input_batch[left_encoder_name][POSITIVE_EMBEDDINGS],
            right_positive_embeddings=right_positive_embeddings,
            right_positive_paddings=right_positive_paddings,
            right_negative_embeddings=input_batch[right_encoder_name].get(
                NEGATIVE_EMBEDDINGS, None
            ),
            right_negative_paddings=input_batch[right_encoder_name].get(NEGATIVE_PADDINGS, None),
        )

    def forward(self, input_batch: NestedTensor) -> NestedTensor:
        """Forward function.

        Args:
            input_batch: A dictionary containing:
                cfg.left_encoder_name:
                    POSITIVE_EMBEDDINGS: A Tensor with shape [batch_size, 1, dim].
                cfg.right_encoder_name:
                    POSITIVE_EMBEDDINGS: A Tensor with shape [batch_size, 1, dim].
                    POSITIVE_PADDINGS: A 0/1 Tensor with shape [batch_size, 1] where 1 means padded
                        docs and 0 means effective docs.
                    NEGATIVE_EMBEDDINGS: A Tensor with shape
                        [batch_size, num_negative_inputs_per_example, dim].
                    NEGATIVE_PADDINGS: A 0/1 Tensor with shape
                        [batch_size, num_negative_inputs_per_example] where 1 means padded docs and
                        0 means effective docs.

        Returns:
            loss: A Tensor representing the loss.
            A dictionary containing:
                SIMILARITY_MATRIX: A Tensor representing the similarity between left encoder
                    embeddings and right encoder embeddings.
        """
        cfg = self.config
        inputs = self._flatten_and_concat_embeddings(input_batch)

        similarity = contrastive_logits(
            inputs[FLATTENED_LEFT_EMBEDDINGS], inputs[FLATTENED_RIGHT_EMBEDDINGS]
        )
        contrastive_loss = asymmetric_contrastive_loss_from_logits(
            similarity,
            key_paddings=inputs[RIGHT_PADDINGS],
            temperature=1 / cfg.contrastive_loss_scale_factor,
        )

        return contrastive_loss, {SIMILARITY_MATRIX: similarity}


class RankingPairwiseLossLayer(FusionNetwork):
    """A FusionNetwork to compute pairwise loss among right encoder pairwise loss candidates based
    on relative ranks.

    The pairwise loss is defined as the binary cross-entropy loss between all possible candidates
    pair for each query. With this loss, model is trained to give higher score to candidate having
    higher rank. For example, (d1, d2, d3) having a rank of (1, 2, 3) could give three pairs for
    learning: (d1, d2), (d1, d3), (d2, d3), where we force model to give higher score to the former
    doc.
    """

    @config_class
    class Config(BaseLayer.Config):
        # Name of left encoder that gives embeddings as queries when computing pairwise loss.
        left_encoder_name: Required[str] = REQUIRED
        # Name of right encoder that gives embeddings as keys when computing pairwise loss.
        right_encoder_name: Required[str] = REQUIRED
        # A positive scalar float to be multiplied with logits. Default is 1.0.
        pairwise_loss_scale_factor: float = 1.0

    def forward(self, input_batch: NestedTensor) -> Tuple[Tensor, Tensor]:
        """Forward function.

        Args:
            input_batch: A dictionary containing:
                LEFT_ENCODER_NAME:
                    POSITIVE_EMBEDDINGS: A Tensor with shape [batch_size, 1, dim].
                RIGHT_ENCODER_NAME:
                    PAIRWISE_LOSS_EMBEDDINGS: A Tensor with shape
                        [batch_size, num_pairwise_loss_inputs_per_examples, dim].
                    PAIRWISE_LOSS_PADDINGS: A 0/1 Tensor with shape
                        [batch_size, num_pairwise_loss_inputs_per_examples] where 1 means padded
                        inputs and 0 means valid inputs.
                    RANKS: An int Tensor with shape
                        [batch_size, num_pairwise_loss_inputs_per_examples] which records ranks of
                        each candidate. Padded candidate will have a rank of 0.

        Returns:
            loss: A scalar Tensor representing the pairwise loss.
            A dictionary:
                NUM_VALID_RANKING_PAIRS: A scalar Tensor indicating the number of valid ranking
                    pairs to calculate pairwise loss.
        """
        cfg = self.config

        left_embeddings = input_batch[cfg.left_encoder_name][POSITIVE_EMBEDDINGS]
        assert (
            left_embeddings.shape[1] == 1
        ), "Expecting one positive embedding per example from left encoder."

        right_embeddings = input_batch[cfg.right_encoder_name][PAIRWISE_LOSS_EMBEDDINGS]
        right_paddings = input_batch[cfg.right_encoder_name][PAIRWISE_LOSS_PADDINGS]

        ranks = input_batch[cfg.right_encoder_name][RANKS]
        num_queries = left_embeddings.shape[0]

        # Shape: [batch_size, 1, num_pairwise_loss_inputs_per_examples].
        logits = jnp.einsum("b i d, b j d -> b i j", left_embeddings, right_embeddings)
        logits = logits * cfg.pairwise_loss_scale_factor
        # Shape: [batch_size, num_pairwise_loss_inputs_per_examples].
        logits = jnp.squeeze(logits, axis=1)

        # Shape: [batch_size, num_pairwise_loss_inputs_per_examples].
        ranks = ranks * (1 - right_paddings)
        loss, num_valid_pairs = ranking_pairwise_loss(
            logits=logits, ranks=ranks, loss_scale=jnp.ones(num_queries)
        )
        return loss, {NUM_VALID_RANKING_PAIRS: num_valid_pairs}


class TextEmbeddingDualEncoder(MultiStreamModel):
    """A basic dual-encoder model for text embedding based applications.

    This class inherits from MultiStreamModel as a two-stream MultiStreamModel.
    Each stream's encoder is expected to be a TextEmbeddingStreamEncoder instance.
    """

    @config_class
    class Config(MultiStreamModel.Config):
        # The name of encoder to be shared in the Siamese encoder case.
        shared_encoder_name: Optional[str] = None

    def __init__(self, cfg: Config, *, parent: Optional[Module]):
        super().__init__(cfg, parent=parent)
        if cfg.shared_encoder_name is not None:
            self._share_with_descendants(
                self._stream_encoder[cfg.shared_encoder_name],
                shared_module_name=TEXT_DUAL_ENCODER_SHARED_MODULE_NAME,
            )

    def _forward_all_stream_encoder(self, input_batch: NestedTensor) -> NestedTensor:
        """Calls the forward function of all the stream encoders."""
        for encoder_name in self._stream_encoder:  # pylint: disable=consider-using-dict-items
            input_batch[encoder_name] = self._stream_encoder[encoder_name](
                input_batch[encoder_name]
            )

        return input_batch

    def forward_single_stream_encoder(
        self, input_batch: NestedTensor, encoder_name: str
    ) -> NestedTensor:
        """Calls the forward function of a specific stream encoders."""
        if encoder_name not in self._stream_encoder:
            raise ValueError(f"{encoder_name} has not been found in stream_encoder.")
        return self._stream_encoder[encoder_name](input_batch[encoder_name])
