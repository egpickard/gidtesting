## Instructions to start the backend server

1. In the command line navigate to the backend/ directory.
2. Run either `python3 main.py` or `uvicorn main:app --reload --port 8080`
   This will start the server on localhost listening at port 8080

## Endpoints to use from frontend

There are two POST endpoints /predict and /mirror\
/predict \
The body of this request should be a json object of the following format: \
`{
"conversation": "string"
}`\
Where conversation contains messages in a two person conversation and changes in speaker are denoted with {-c-s-}. For example: \
`{
"conversation": "hey whats up{-c-s-}not much, you{-c-s-}same same{-c-s-}ok by{-c-s-}goodby"
}`\
The response will be a json object of the following format: \
`{
"pred": 0
}`\
With pred being 0 if grooming is not detected and 1 if grooming is detected.\
/mirror\
The body of this request should be a json object of the following format: \
`{
"text": "string"
}`\
The response will be: \
`{
"text": "string"
}`\
This endpoint just returns the input back to the user and can be used for testing to ensure that communication is occuring between the webpage and the server.
