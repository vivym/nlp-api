import os
from concurrent import futures

import sentry_sdk
import grpc

from nlp.model import nlp_pb2, nlp_pb2_grpc
from nlp.keyword import tf_idf, text_rank


class NLPServer(nlp_pb2_grpc.NLPServicer):
    def extract(self, method, sentence, top_k, allow_pos):
        if method == nlp_pb2.KeywordRequest.MethodType.TFIDF:
            extractor = tf_idf
        else:
            extractor = text_rank

        words = extractor(
            sentence, top_k=top_k, allow_pos=allow_pos
        )

        def to_keyword(keyword):
            return nlp_pb2.KeywordResponse.Keyword(**keyword)

        return nlp_pb2.KeywordResponse(
            keywords=list(map(to_keyword, words))
        )

    def ExtractKeywords(self, request, context):
        return self.extract(
            method=request.method,
            sentence=request.sentence,
            top_k=request.topK,
            allow_pos=request.allowPOS,
        )

    def ExtractKeywordsStream(self, request_iterator, context):
        method = nlp_pb2.KeywordRequest.MethodType.TFIDF
        sentence = ""
        top_k = 20
        allow_pos = []

        for request in request_iterator:
            method = request.method
            top_k = request.topK
            allow_pos = request.allowPOS

            sentence += "\n" + request.sentence

        return self.extract(method, sentence, top_k, allow_pos)


def main():
    sentry_dsn = os.getenv("APP_SENTRYDSN") or ""
    grpc_port = os.getenv("APP_GRPC_PORT") or "12377"

    sentry_sdk.init(sentry_dsn)

    server = grpc.server(futures.ThreadPoolExecutor())

    nlp_pb2_grpc.add_NLPServicer_to_server(NLPServer(), server)

    server.add_insecure_port("0.0.0.0:" + grpc_port)
    server.start()

    print("listening on port: " + grpc_port)

    server.wait_for_termination()


if __name__ == "__main__":
    main()
