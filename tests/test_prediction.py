import pytest

import dawg_python
from .utils import data_path


class TestPrediction:

    REPLACES = dawg_python.DAWG.compile_replaces({'Е': 'Ё'})

    DATA = ['ЁЖИК', 'ЁЖИКЕ', 'ЁЖ', 'ДЕРЕВНЯ', 'ДЕРЁВНЯ', 'ЕМ', 'ОЗЕРА', 'ОЗЁРА', 'ОЗЕРО']
    SUITE = [
        ('УЖ', []),
        ('ЕМ', ['ЕМ']),
        ('ЁМ', []),
        ('ЁЖ', ['ЁЖ']),
        ('ЕЖ', ['ЁЖ']),
        ('ЁЖИК', ['ЁЖИК']),
        ('ЕЖИКЕ', ['ЁЖИКЕ']),
        ('ДЕРЕВНЯ', ['ДЕРЕВНЯ', 'ДЕРЁВНЯ']),
        ('ДЕРЁВНЯ', ['ДЕРЁВНЯ']),
        ('ОЗЕРА', ['ОЗЕРА', 'ОЗЁРА']),
        ('ОЗЕРО', ['ОЗЕРО']),
    ]

    SUITE_ITEMS = [
        (
            it[0],  # key
            [(w, [(len(w),)]) for w in it[1]],  # item, value pair
        )
        for it in SUITE
    ]

    SUITE_VALUES = [
        (
            it[0],  # key
            [[(len(w),)] for w in it[1]],
        )
        for it in SUITE
    ]

    def record_dawg(self):
        path = data_path("small", "prediction-record.dawg")
        return dawg_python.RecordDAWG("=H").load(path)

    @pytest.mark.parametrize(("word", "prediction"), SUITE)
    def test_dawg_prediction(self, word, prediction):
        d = dawg_python.DAWG().load(data_path("small", "prediction.dawg"))
        assert d.similar_keys(word, self.REPLACES) == prediction

    @pytest.mark.parametrize(("word", "prediction"), SUITE)
    def test_record_dawg_prediction(self, word, prediction):
        d = self.record_dawg()
        assert d.similar_keys(word, self.REPLACES) == prediction

    @pytest.mark.parametrize(("word", "prediction"), SUITE_ITEMS)
    def test_record_dawg_items(self, word, prediction):
        d = self.record_dawg()
        assert d.similar_items(word, self.REPLACES) == prediction

    @pytest.mark.parametrize(("word", "prediction"), SUITE_VALUES)
    def test_record_dawg_items_values(self, word, prediction):
        d = self.record_dawg()
        assert d.similar_item_values(word, self.REPLACES) == prediction
