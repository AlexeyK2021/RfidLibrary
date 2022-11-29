class work:
    waiting = 0
    take_book = 1
    return_book = 2
    off = 3
    curr_state = 0

    def take_button(self):
        if self.curr_state == self.waiting:
            self.curr_state = self.take_book
        elif self.curr_state == self.take_book:
            self.curr_state = self.waiting
        elif self.curr_state == self.return_book:
            self.curr_state = self.take_book

    def return_button(self):
        if self.curr_state == self.waiting:
            self.curr_state = self.return_book
        elif self.curr_state == self.return_book:
            self.curr_state = self.waiting
        elif self.curr_state == self.take_book:
            self.curr_state = self.return_book

    def switch_off(self):
        self.curr_state = self.off

    def switch_waiting(self):
        self.curr_state = self.waiting
