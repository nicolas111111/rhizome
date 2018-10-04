""""""
from bbot.core import ChatbotEngine

class DotFlow2CoreFunctions():
    """."""

    def __init__(self, bot: ChatbotEngine) -> None:
        """
        """

        self.bot = bot
        self.functions = ['input', 'eq', 'code']

        for f in self.functions:
            bot.register_dotflow2_function(f, {'object': self, 'method': f})
            bot.register_template_function(f, {'object': self, 'method': f})



    ####################################################################################################################


    def code(self, args, f_type):
        """
        !!!!WARNING!!!! THIS FUNCTION RUNS UNRESTRICTED PYTHON CODE. DON'T EXPOSE IT TO PUBLIC ACCESS!!

        This functions is used to run any python code on conditions and responses objects.
        Of course you can use DotFlow2 functions inside it
        :param args:    0: string with python code
                        1: boolean. True to get expression result (only expressions works). False to run any kind of python code
        :return:
        """
        code = args[0]
        if type(code) is not str:
            raise Exception('$code: Arg should be string')

        # Transpile $python code into Python code ready to run in DotFlow2 environment
        for f in self.bot.dotflow2_functions_map:
            # shortcut: no need to prefix "self.bot.df2." on all Dotflow2 functions
            code = code.replace(f + '(', 'self.bot.df2.' + f + '(')

        self.bot.logger_df2.debug('Running python code: "' + code + "'...")
        result = None
        if f_type == 'C':           # If it's called from Condition object we need a result from the expression
            result = eval(code)
        elif f_type == 'R':         # If it's called from Responses object we need to freely run the code. No expression returned
            exec(code)

        self.bot.logger_df2.debug('Returning: ' + str(result))
        return result


    def input(self, args, f_type):
        """
        Returns user input

        :return:
        """
        return self.bot.request['input']['text']

    def eq(self, args, f_type):
        """
        Evaluates equivalency between two args
        :return:
        """

        if type(args[0]) is str and type(args[1]) is str:
            response = args[0].strip().lower() == args[1].strip().lower()
        elif args[0].isdigit() and args[0].isdigit():
            response = args[0] == args[1]
        else:
            raise Exception('$eq: Args are not strings or numbers')
        return response
