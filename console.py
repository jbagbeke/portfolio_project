#!/usr/bin/python3
"""
    The console for the portfolio project
                                        """
from models.user import User
from models import storage
from models.message import Message
from models.recipient import Recipient
import cmd


class PORTCMD(cmd.Cmd):
    """
        The console for backend testing
                                        """
    prompt = '(portfolio) '

    def do_create(self, arg):
        """
            Creates class instances
                                    """

        args = arg.split()

        if len(args) == 0:
            print("** class name missing **")
            return False

        if len(args) == 1:
            print("** class arguments missing ** ")
            return False

        new_dict = {}
        args[1] = args[1].replace('_', ' ')

        for name in args[1:]:
            key, value = name.split('=')
            new_dict[key] = value

        print(new_dict)
        if args[0] == 'User':
           user_id = User._UserID()
           new_dict['user_id'] = str(user_id)

        if args[0] == 'Message':
            if not new_dict.get('user_id'):
                print("** User ID missing/incorrect **")
                return False

            if not new_dict.get('receiver_number'):
                print("** Receiver Number Missing **")
                return False

            recipient_number = new_dict.get('receiver_number')
            del new_dict['receiver_number']

            user_id = new_dict.get('user_id')
            user_obj = storage.get(User, user_id)
            print(user_obj)
            new_instance = globals().get(args[0])(user=user_obj, **new_dict)
        else:
            new_instance = globals().get(args[0])(**new_dict)

        if args[0] == 'Message':
            recipient_obj = Recipient(user_id=user_obj.id,
                                      message_id=new_instance.id,
                                      receiver_number=recipient_number,
                                      message=new_instance,
                                      user=user_obj)
            print("RECIPIENT::\n", recipient_obj, '\n')

            #new_instance.user = list(user_obj)
            #new_instance.recipient = recipient_obj

            #user_obj.messages = new_instance


        print(new_instance.id)
        storage.new(new_instance)
        storage.save()

    def do_all(self, arg):
        """
            Retrieves all instances of a class
                                                """
        args = arg.split()

        if len(args) == 0:
            all_objects = storage.all()

        if len(args) == 1:
            all_objects = storage.all(args[0])

        print(all_objects)

    def emptyline(self, arg):
        """
            Do nothing if no input is entered
                                            """
        pass

    def do_EOF(self, arg):
        """
            Handles End Of File to exit the program
                                                    """
        print('')
        exit()

if __name__ == '__main__':
        PORTCMD().cmdloop()
