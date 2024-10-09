
from ariadne import QueryType, MutationType, make_executable_schema
from ariadne.asgi import GraphQL
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from PIL import Image
import torch
import io
import uvicorn

# Load your custom YOLOv8 model (assuming the model file is named 'best.pt' and located in the appropriate directory)
model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt')

# Query and Mutation types
query = QueryType()
mutation = MutationType()

# Sample query example
@query.field("hello")
def resolve_hello(_, info):
    return "안녕하세요! GraphQL 서버입니다."

# Mutation to handle image upload and object detection
@mutation.field("uploadImage")
async def resolve_upload_image(_, info, file):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    
    # Run object detection on the image
    results = model(image)
    
    # Process detection results
    detections = results.pandas().xyxy[0]  # Extract results in pandas DataFrame format
    object_counts = detections['name'].value_counts().to_dict()  # Count occurrences of each detected object
    
    return {"detections": object_counts}

# GraphQL schema definition as a properly formatted string
type_defs = '''
type Query {
    hello: String!
}

type Mutation {
    uploadImage(file: Upload!): DetectionResult!
}

type DetectionResult {
    detections: JSON!
}
'''

# Create executable schema
schema = make_executable_schema(type_defs, query, mutation)

# Create Starlette application
app = Starlette()

# CORS settings (allow all domains)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# GraphQL endpoint setup with GraphQL Playground enabled
app.add_route("/graphql", GraphQL(schema, debug=True))

# Application entry point
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
