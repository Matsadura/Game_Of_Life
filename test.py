#!/usr/bin/python3
import tkinter as tk


class InfiniteCanvas(tk.Canvas):
    """
    Initial idea by Nordine Lofti
    https://stackoverflow.com/users/12349101/nordine-lotfi
    written by Thingamabobs
    https://stackoverflow.com/users/13629335/thingamabobs

    The infinite canvas allows you to have infinite space to draw.

    You can move around the world as follows:
    - MouseWheel for Y movement.
    - Shift-MouseWheel will perform X movement.
    - Alt-Button-1-Motion will perform X and Y movement.
    (pressing ctrl while moving will invoke a multiplier)

    Additional features to the standard tk.Canvas:
    - Keeps track of the viewable area
    --> Acess via InfiniteCanvas().viewing_box()
    - Keeps track of the visibile items
    --> Acess via InfiniteCanvas().inview()
    - Keeps track of the NOT visibile items
    --> Acess via InfiniteCanvas().outofview()

    Also a new standard tag is introduced to the Canvas.
    All visible items will have the tag "inview"
    """

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self._xshifted = 0  # view moved in x direction
        self._yshifted = 0  # view moved in y direction
        self.configure(confine=False, highlightthickness=0, bd=0)
        self.bind("<MouseWheel>", self._vscroll)
        self.bind("<Shift-MouseWheel>", self._hscroll)
        self.winfo_toplevel().bind("<KeyPress-Alt_L>", self._alternate_cursor)
        self.winfo_toplevel().bind("<KeyRelease-Alt_L>", self._alternate_cursor)
        self.bind("<ButtonPress-1>", self._start_drag_scroll)
        self.bind("<Alt-B1-Motion>", self._drag_scroll)
        return None

    def viewing_box(self) -> tuple:
        "Returns a tuple of the form x1,y1,x2,y2 represents visible area"
        x1 = 0 - self._xshifted
        y1 = 0 - self._yshifted
        x2 = self.winfo_reqwidth() - self._xshifted
        y2 = self.winfo_reqheight() - self._yshifted
        return x1, y1, x2, y2

    def inview(self) -> set:
        "Returns a set of identifiers that are currently viewed"
        return set(self.find_overlapping(*self.viewing_box()))

    def outofview(self) -> set:
        "Returns a set of identifiers that are currently viewed"
        all_ = set(self.find_all())
        return all_ - self.inview()

    def _alternate_cursor(self, event):
        if (et := event.type.name) == "KeyPress":
            self.configure(cursor="fleur")
        elif et == "KeyRelease":
            self.configure(cursor="")

    def _update_tags(self):
        vbox = self.viewing_box()
        self.addtag_overlapping("inview", *vbox)
        inbox = set(self.find_overlapping(*vbox))
        witag = set(self.find_withtag("inview"))
        [self.dtag(i, "inview") for i in witag - inbox]
        self.viewing_box()

    def _create(self, *args):
        ident = super()._create(*args)
        self._update_tags()
        return ident

    def _wheel_scroll(self, xy, amount):
        cx, cy = self.winfo_rootx(), self.winfo_rooty()
        self.scan_mark(cx, cy)
        if xy == "x":
            x, y = cx + amount, cy
        elif xy == "y":
            x, y = cx, cy + amount
        name = f"_{xy}shifted"
        setattr(self, name, getattr(self, name) + amount)
        self.scan_dragto(x, y, gain=1)
        self._update_tags()

    def _drag_scroll(self, event):
        xoff = event.x - self._start_drag_point_x
        yoff = event.y - self._start_drag_point_y
        self._xshifted += xoff
        self._yshifted += yoff
        gain = 1
        if (event.state & 0x4) != 0:  # if ctr/strg
            gain = 2
        self.scan_dragto(event.x, event.y, gain=gain)
        self._start_drag_point_x = event.x
        self._start_drag_point_y = event.y
        self._update_tags()

    def _start_drag_scroll(self, event):
        self._start_drag_point_x = event.x
        self._start_drag_point_y = event.y
        self.scan_mark(event.x, event.y)
        return

    def _hscroll(self, event):
        offset = int(event.delta / 120)
        if (event.state & 0x4) != 0:  # if ctr/strg
            offset = int(offset * 10)
        self._wheel_scroll("x", offset)

    def _vscroll(self, event):
        offset = int(event.delta / 120)
        if (event.state & 0x4) != 0:  # if ctr/strg
            offset = int(offset * 10)
        self._wheel_scroll("y", offset)


if __name__ == "__main__":
    root = tk.Tk()
    canvas = InfiniteCanvas(root)
    canvas.pack(fill=tk.BOTH, expand=True)

    size, offset, start = 100, 10, 0
    canvas.create_rectangle(start, start, size, size, fill="green")
    canvas.create_rectangle(
        start + offset, start + offset, size + offset, size + offset, fill="darkgreen"
    )

    root.mainloop()
