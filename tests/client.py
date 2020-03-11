import os

import grpc

from nlp.model import nlp_pb2, nlp_pb2_grpc

allow_pos = (
    'n',
    'nr',
    'nz',
    'ns',
    'v',
    's',
    'nt',
    'nw',
    'vn',
)


def keyword_extract(stub, text):
    print("keyword_extract:")
    req = nlp_pb2.KeywordRequest(
        method=nlp_pb2.KeywordRequest.TextRank,
        sentence=text,
        topK=5,
        allowPOS=allow_pos,
    )

    keywords = stub.KeywordExtract(req).keywords

    for keyword in keywords:
        print(keyword.word, keyword.weight, keyword.pos)


def keyword_extract_stream(stub, text):
    print("keyword_extract_stream:")

    sentences = list(filter(lambda x: len(x), text.split("\n")))

    def request_generator():
        for sentence in sentences:
            req = nlp_pb2.KeywordRequest(
                method=nlp_pb2.KeywordRequest.TFIDF,
                sentence=sentence,
                topK=5,
            )
            yield req

    keywords = stub.KeywordExtractStream(request_generator()).keywords

    for keyword in keywords:
        print(keyword.word, keyword.weight, keyword.pos)


def main():
    with grpc.insecure_channel("localhost:12377") as channel:
        stub = nlp_pb2_grpc.NLPStub(channel)
        
        text = open(os.path.join(os.path.dirname(__file__), "test.txt")).read()

        keyword_extract(stub, text)

        keyword_extract_stream(stub, text)


if __name__ == "__main__":
    main()
