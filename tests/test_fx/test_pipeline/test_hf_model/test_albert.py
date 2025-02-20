import transformers
import torch
from hf_utils import split_model_and_compare_output

BATCH_SIZE = 2
SEQ_LENGHT = 16


def test_single_sentence_albert():
    MODEL_LIST = [
        transformers.AlbertModel,
        transformers.AlbertForPreTraining,
        transformers.AlbertForMaskedLM,
        transformers.AlbertForSequenceClassification,
        transformers.AlbertForTokenClassification,
    ]

    config = transformers.AlbertConfig(vocab_size=100,
                                       embedding_size=128,
                                       hidden_size=128,
                                       num_hidden_layers=2,
                                       num_attention_heads=4,
                                       intermediate_size=256)

    def data_gen():
        input_ids = torch.zeros((BATCH_SIZE, SEQ_LENGHT), dtype=torch.int64)
        token_type_ids = torch.zeros((BATCH_SIZE, SEQ_LENGHT), dtype=torch.int64)
        attention_mask = torch.zeros((BATCH_SIZE, SEQ_LENGHT), dtype=torch.int64)
        meta_args = dict(input_ids=input_ids, token_type_ids=token_type_ids, attention_mask=attention_mask)
        return meta_args

    for model_cls in MODEL_LIST:
        model = model_cls(config=config)
        split_model_and_compare_output(model, data_gen)


if __name__ == '__main__':
    test_single_sentence_albert()
