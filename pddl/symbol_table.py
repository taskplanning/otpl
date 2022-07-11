class SymbolTable:

    def __init__(self):
        self.symbol_table = {}
        self.symbol_list = []

    def get_symbol(self, id):
        """
        Returns the symbol for the given id.
        :param id: The id of the symbol.
        :return: The symbol.
        """
        if len(self.symbol_list) <= id:
            return None
        return self.symbol_list[id]

    def get_symbol_id(self, symbol):
        """
        Returns the id of the given symbol.
        :param symbol: The symbol to get the id of.
        :return: The id of the symbol.
        """
        if symbol not in self.symbol_table:
            return None
        return self.symbol_table[symbol]

    def add_symbol(self, symbol):
        """
        Adds a symbol to the symbol table.
        :param symbol: The symbol to add.
        :return: The id of the symbol.
        """
        if symbol not in self.symbol_table:
            self.symbol_list.append(symbol)
            self.symbol_table[symbol] = len(self.symbol_list) - 1
        return self.symbol_table[symbol]