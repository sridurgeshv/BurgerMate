import json

burger_sizes = ['Mini', 'Standard', 'Big']
burger_types = ['Vegetarian', 'Non-vegetarian']
vegburger_types = ['Lentil Patty', 'Fresh vegetables', 'Portobello mushrooms']
nvegburger_types = ['Chicken', 'Beef', 'Pork']
side_types = ['Fries', 'Onion Rings', 'Cucumber salad']
drink_types = ['Soda', 'Coca-Cola', 'Pepsi']


def validate_order(slots):
    if not slots['BurgerSize']:
        print('Validating BurgerSize Slot')
        return {
            'isValid': False,
            'invalidSlot': 'BurgerSize'
        }

    if slots['BurgerSize']['value']['originalValue'] not in burger_sizes:
        print('Invalid BurgerSize')
        return {
            'isValid': False,
            'invalidSlot': 'BurgerSize',
            'message': 'Please select a {} burger size.'.format(", ".join(burger_sizes))
        }

    if not slots['BurgerType']:
        print('Validating BurgerType Slot')
        return {
            'isValid': False,
            'invalidSlot': 'BurgerType'
        }

    if slots['BurgerType']['value']['originalValue'] not in burger_types:
        print('Invalid BurgerType')
        return {
            'isValid': False,
            'invalidSlot': 'BurgerType',
            'message': 'Please select a vegetarian or non-vegetarian burger.'
        }

    if slots['BurgerType']['value']['originalValue'] == 'Vegetarian':
        if not slots['Vegburger']:
            print('Validating Vegburger Slot')
            return {
                'isValid': False,
                'invalidSlot': 'Vegburger'
            }
        if slots['Vegburger']['value']['originalValue'] not in vegburger_types:
            print('Invalid Vegburger Type')
            return {
                'isValid': False,
                'invalidSlot': 'Vegburger',
                'message': 'Please select a veggie patty type of {}.'.format(", ".join(vegburger_types))
            }

    if slots['BurgerType']['value']['originalValue'] == 'Non-vegetarian':
        if not slots['NvegBurger']:
            print('Validating NvegBurger Slot')
            return {
                'isValid': False,
                'invalidSlot': 'NvegBurger'
            }
        if slots['NvegBurger']['value']['originalValue'] not in nvegburger_types:
            print('Invalid NvegBurger Type')
            return {
                'isValid': False,
                'invalidSlot': 'NvegBurger',
                'message': 'Please select a non-veggie patty type of {}.'.format(", ".join(nvegburger_types))
            }

    if not slots['SideType']:
        print('Validating SideType Slot')
        return {
            'isValid': False,
            'invalidSlot': 'SideType'
        }

    if slots['SideType']['value']['originalValue'] not in side_types:
        print('Invalid SideType')
        return {
            'isValid': False,
            'invalidSlot': 'SideType',
            'message': 'Please select a side type of {}.'.format(", ".join(side_types))
        }

    if not slots['DrinkType']:
        print('Validating DrinkType Slot')
        return {
            'isValid': False,
            'invalidSlot': 'DrinkType'
        }

    if slots['DrinkType']['value']['originalValue'] not in drink_types:
        print('Invalid DrinkType')
        return {
            'isValid': False,
            'invalidSlot': 'DrinkType',
            'message': 'Please select a drink type of {}.'.format(", ".join(drink_types))
        }

    return {'isValid': True}


def lambda_handler(event, context):
    print(event)

    bot = event['bot']['name']
    slots = event['sessionState']['intent']['slots']
    intent = event['sessionState']['intent']['name']

    order_validation_result = validate_order(slots)

    if event['invocationSource'] == 'DialogCodeHook':
        if not order_validation_result['isValid']:
            if 'message' in order_validation_result:
                response = {
                    "sessionState": {
                        "dialogAction": {
                            "slotToElicit": order_validation_result['invalidSlot'],
                            "type": "ElicitSlot"
                        },
                        "intent": {
                            "name": intent,
                            "slots": slots
                        }
                    },
                    "messages": [
                        {
                            "contentType": "PlainText",
                            "content": order_validation_result['message']
                        }
                    ]
                }
            else:
                response = {
                    "sessionState": {
                        "dialogAction": {
                            "slotToElicit": order_validation_result['invalidSlot'],
                            "type": "ElicitSlot"
                        },
                        "intent": {
                            "name": intent,
                            "slots": slots
                        }
                    }
                }
        else:
            response = {
                "sessionState": {
                    "dialogAction": {
                        "type": "Delegate"
                    },
                    "intent": {
                        'name': intent,
                        'slots': slots
                    }
                }
            }

    if event['invocationSource'] == 'FulfillmentCodeHook':
        response = {
            "sessionState": {
                "dialogAction": {
                    "type": "Close"
                },
                "intent": {
                    "name": intent,
                    "slots": slots,
                    "state": "Fulfilled"
                }

            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": "I've placed your order."
                }
            ]
        }

    print(response)
    return response
