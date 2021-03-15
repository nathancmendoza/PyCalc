import tkinter as tk
from interpreter import Interpretor

class CalculatorApp(tk.Tk):
    height = 700
    width = 500
    buttons = ('e', 'ln', 'log', 'clear', 
               'π','arcsin', 'arccos', 'arctan', 
               '√', 'sin', 'cos', 'tan',
               '^', '(', ')', '/',
               '7', '8', '9', '*',
               '4', '5', '6', '-',
               '1', '2', '3', '+',
               '0', '.', 'ans', '=')
    
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry(f'{self.width}x{self.height}')
        self._define_display_string()
        self._define_equation_solver()
        self.resizable = True
        self.title('Calculator App')
        self.create_widgets()
        self.arrange_widgets()
        self._bind_keys()

    def _define_display_string(self):
        self.display_string = tk.StringVar()
        self.display_string.set('')

    def _define_equation_solver(self):
        self.equation_solver = Interpretor()
       
    def create_widgets(self):
        self._create_display_frame()
        self._create_display_box()

        self._create_buttons_display_frame()
        self._create_buttons()

    def arrange_widgets(self):
        self.calculator_display.pack(side=tk.TOP, 
                                 fill=tk.BOTH, 
                                 expand=True)
        self.display_msg.pack(fill=tk.BOTH, 
                              expand=True)


        self.buttons_display.pack(side=tk.BOTTOM, 
                                  fill=tk.BOTH, 
                                  expand=True)
        self._show_buttons()
        
    def _create_display_frame(self):
        self.calculator_display = self._create_frame(self, 
                                                 bg='#a2aeb8', 
                                                 padx=10, 
                                                 pady=10,
                                                 height=int(0.2 * self.height)) 
        
        
    def _create_display_box(self):
        self.display_msg = self._create_lbl(self.calculator_display, 
                                            bg='#70998a',
                                            fg='#01394a',
                                            anchor=tk.W, 
                                            relief=tk.SUNKEN,
                                            font=('Consolas',28),
                                            textvariable=self.display_string)

    def _create_buttons_display_frame(self):
        self.buttons_display = self._create_frame(self, 
                                                  bg='#a2aeb8', 
                                                  height=int(0.8 * self.height))
        for i in range(4):
            self.buttons_display.columnconfigure(i, weight=1, minsize=6)

        for j in range(8):
            self.buttons_display.rowconfigure(j, weight=2, minsize=2)

    def _create_buttons(self):
        self._buttons = [self._create_btn(self.buttons_display, 
                                          bg='#658fad', 
                                          text=i,
                                          width=6,
                                          height=2,
                                          font=('Consolas', 16),
                                          relief=tk.RAISED) 
                                          for i in self.buttons]
        self._set_button_actions()

    def _set_button_action(self, action):
        if action == '=':
            def _solve():
                self.equation_solver.set_expression(self.display_string.get())
                try:
                    self.equation_solver.solve()
                except ValueError:
                    self.display_string.set('Domain Error')
                except ZeroDivisionError:
                    self.display_string.set('Divide by 0 Error')
                except (SyntaxError, NameError, AttributeError):
                    self.display_string.set('Syntax Error')
                else:
                    self.display_string.set(self.equation_solver.ans)
                finally:
                    self.equation_solver.clear_expression()

            return _solve
        if action == 'clear':
            def _clear():
                self.display_string.set('')

            return _clear
        def _do():
            self.display_string.set(self.display_string.get() + action)

        return _do

    def _set_button_actions(self):
        for btn in self._buttons:
            do = self._set_button_action(btn['text'])
            btn.configure(command=do)
            
    def _show_buttons(self):
        r, c = 0, 0
        for btn in self._buttons:
            btn.grid(row=r, column=c, padx=3, pady=1)

            if c == 3:
                r += 1
                c = 0
                continue
            c += 1

    def _bind_keys(self):
        self.bind('<Key>', self._allowed_keys)
        self.bind('<Return>', self._enter_key)
        self.bind('<BackSpace>', self._backspace_key)
        

    def _allowed_keys(self, event):
        allowed_keys = ('1', '2', '3',
                        '4', '5', '6',
                        '7', '8', '9',
                        '+', '-', '*',
                        '/', '(', ')',
                        '.', 'e', '0')
        if event.char in allowed_keys:
            self.display_string.set(self.display_string.get() + event.char)

    def _enter_key(self, event):
        self.equation_solver.set_expression(self.display_string.get())
        try:
            self.equation_solver.solve()
        except ValueError:
            self.display_string.set('Domain Error')
        except ZeroDivisionError:
            self.display_string.set('Divide by 0 Error')
        except (SyntaxError, NameError, AttributeError):
            self.display_string.set('Syntax Error')
        else:
            self.display_string.set(self.equation_solver.ans)
        finally:
            self.equation_solver.clear_expression()
    
    def _backspace_key(self, event):
        self.display_string.set(self.display_string.get()[:-1])
   
    @staticmethod
    def _create_btn(parent, **config):
        return tk.Button(parent, **config)
     
    @staticmethod
    def _create_lbl(parent, **config):
        return tk.Label(parent, config)

    @staticmethod
    def _create_frame(parent, **config):
        return tk.Frame(parent, **config)
            
    def launch(self):
        self.mainloop()


if __name__ == '__main__':
    app = CalculatorApp()
    app.launch()