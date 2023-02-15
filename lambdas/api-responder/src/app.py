"""
Simple Python Lambda function to respond to GET requests
"""
from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler.api_gateway import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.exceptions import (
    BadRequestError,
    InternalServerError,
    NotFoundError,
    # ServiceError,
    # UnauthorizedError,
)
from aws_lambda_powertools.logging import correlation_paths

logger = Logger(log_uncaught_exceptions=True) # Sets service via env var
app = APIGatewayRestResolver()


@app.exception_handler(AssertionError)
def handle_assertion_errors(ex: AssertionError):
    raise BadRequestError(str(ex))


@app.get(".+", compress=True) # catch-all route
def catch_any_route_get_method():
    assert app.current_event.get_query_string_value(name="isTest", default_value="true") == "true", 'missing "isTest" query string parameter'
    return {"path_received": app.current_event.path}


@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST)
def lambda_handler(event, context):
    return app.resolve(event, context)
