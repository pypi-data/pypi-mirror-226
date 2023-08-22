import functions_framework
import collections.abc

@functions_framework.http
def bot(**kwargs):
    def bot_message(func):
        def bot_function(*args, **kwargs_func):
            print('name of the bot: ', kwargs['name'])
            request = args[0]
            post_body = request.json
            messages = post_body['data']['messages']
            state = post_body['data']['state']

            if not isinstance(messages, collections.abc.Sequence):
                return 'Error in processing', 402

            resp = func(messages, state)

            return resp
        return bot_function
    return bot_message