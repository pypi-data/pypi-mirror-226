class RabbitMQConnectionFailed(Exception):
    pass


class RabbitMQServerError(Exception):
    pass


def publish(msg):
    if msg == '1':
        raise RabbitMQConnectionFailed("connection failed")
    elif msg == '2':
        raise RabbitMQServerError("Server error")
    else:
        raise Exception('unknown error')


if __name__ == '__main__':
    try:
        publish('2')
    except (Exception, RabbitMQConnectionFailed, RabbitMQServerError) as e:
        print(f'Error: {str(e)}, Type: {type(e)}')


"""
OUTPUT:
Error: Server error, Type: <class '__main__.RabbitMQServerError'>

"""