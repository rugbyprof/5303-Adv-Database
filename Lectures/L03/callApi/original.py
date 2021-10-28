#https://stackoverflow.com/questions/44736279/kivy-gridlayout-always-goes-left-to-right-then-down-can-you-go-top-to-bottom-t?rq=1
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


def nmax(*args):
    # merge into one list
    args = [x for x in args if x is not None]
    return max(args)


def nmin(*args):
    # merge into one list
    args = [x for x in args if x is not None]
    return min(args)

class TBGridLayout(GridLayout):
    
    def _fill_rows_cols_sizes(self):
        cols, rows = self._cols, self._rows
        cols_sh, rows_sh = self._cols_sh, self._rows_sh
        cols_sh_min, rows_sh_min = self._cols_sh_min, self._rows_sh_min
        cols_sh_max, rows_sh_max = self._cols_sh_max, self._rows_sh_max

        # calculate minimum size for each columns and rows
        n_rows = len(rows)
        has_bound_y = has_bound_x = False
        for i, child in enumerate(reversed(self.children)):
            (shw, shh), (w, h) = child.size_hint, child.size
            shw_min, shh_min = child.size_hint_min
            shw_max, shh_max = child.size_hint_max
            col,  row = divmod(i, n_rows)

            # compute minimum size / maximum stretch needed
            if shw is None:
                cols[col] = nmax(cols[col], w)
            else:
                cols_sh[col] = nmax(cols_sh[col], shw)
                if shw_min is not None:
                    has_bound_x = True
                    cols_sh_min[col] = nmax(cols_sh_min[col], shw_min)
                if shw_max is not None:
                    has_bound_x = True
                    cols_sh_max[col] = nmin(cols_sh_max[col], shw_max)

            if shh is None:
                rows[row] = nmax(rows[row], h)
            else:
                rows_sh[row] = nmax(rows_sh[row], shh)
                if shh_min is not None:
                    has_bound_y = True
                    rows_sh_min[col] = nmax(rows_sh_min[col], shh_min)
                if shh_max is not None:
                    has_bound_y = True
                    rows_sh_max[col] = nmin(rows_sh_max[col], shh_max)
        self._has_hint_bound_x = has_bound_x
        self._has_hint_bound_y = has_bound_y
       
    def _iterate_layout(self, count):
        selfx = self.x
        padding_left = self.padding[0]
        padding_top = self.padding[1]
        spacing_x, spacing_y = self.spacing

        i = count - 1
        x = selfx + padding_left
        
        for col_width in self._cols:
            y = self.top - padding_top
            for row_height in self._rows:
                if i < 0:
                    break
                yield i, x, y - row_height, col_width, row_height
                i -=  1
                y -=  spacing_y + row_height
            x += col_width + spacing_x
            
# EXAMPLE OF USE    
class MainWindow(BoxLayout):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.orientation = 'vertical'
        self.layout = TBGridLayout(rows=5)
        self.add_widget(self.layout)
        
        self.cont = 0
        self.add_widget(Button(text='Add Button',
                               size_hint = (1,  0.15),  
                               on_press= self.add_button))

        
    def add_button(self,  instance):
        self.cont += 1
        self.layout.add_widget(Button(text = 'Button' + str(self.cont)))

class ExampleApp(App):
    def build(self):
        return MainWindow()

if __name__ == "__main__":
    ExampleApp().run()