from ariadne import QueryType, make_executable_schema
from ariadne.asgi import GraphQL
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware

# 쿼리 타입 정의
query = QueryType()

# 간단한 쿼리 예시
@query.field("hello")
def resolve_hello(_, info):
    return "안녕하세요! GraphQL 서버입니다."

# GraphQL 스키마 정의
type_defs = """
    type Query {
        hello: String!
    }
"""

# 스키마 생성
schema = make_executable_schema(type_defs, query)

# Starlette 애플리케이션 생성
app = Starlette()

# CORS 설정 (모든 도메인 허용)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# GraphQL 엔드포인트 설정 및 GraphQL Playground 활성화
app.add_route("/graphql", GraphQL(schema, debug=True))

# 애플리케이션 실행
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
