from typing import List

import jieba.analyse
import jieba.posseg


def _convert(obj):
    if isinstance(obj[0], jieba.posseg.pair):
        word = obj[0].word
        pos = obj[0].flag
    else:
        word = obj[0]
        pos = ""
    return {
        "word": word,
        "weight": obj[1],
        "pos": pos,
    }


def tf_idf(sentence: str, top_k: int, allow_pos: List[str]) -> List:
    words = jieba.analyse.extract_tags(
        sentence, topK=top_k, withWeight=True,
        allowPOS=allow_pos, withFlag=True,
    )

    return list(map(_convert, words))


def text_rank(sentence: str, top_k: int, allow_pos: List[str]) -> List:
    words = jieba.analyse.textrank(
        sentence, topK=top_k, withWeight=True,
        allowPOS=allow_pos, withFlag=True,
    )

    return list(map(_convert, words))
