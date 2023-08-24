import functions_framework

@functions_framework.http
def bot(**kwargs):
    def bot_message(func):
        def bot_function(*args, **kwargs_func):
            request = args[0]
            post_body = request.json
            messages = post_body['data']['messages']
            state = post_body['data']['state']

            if not isinstance(messages, list):
                return 'Error in processing', 402

            resp = func(messages, state)

            return resp
        return bot_function
    return bot_message