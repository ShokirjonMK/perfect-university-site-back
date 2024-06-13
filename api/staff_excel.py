import xlwt
from django.utils import timezone
from rest_framework import generics

from admin_panel.model.ministry import Staff
from django.http import HttpResponse


class ExcelHelperMixin:
    center_horiz_vert_text = "align: horizontal center, vertical center;"
    black_font = "font: color black;"
    white_font = "font: color white;"

    black_border_text = "borders: top_color black, bottom_color black, right_color black, left_color black,\
                                            left thin, right thin, top thin, bottom thin;\
                                   pattern: pattern solid, fore_color white;"
    rotate_90 = "align: rotation 90;"

    gray_background_text = "pattern: pattern solid, fore_colour gray_color;"

    xlwt.add_palette_colour("gray_color", 0x21)

    gray_style = xlwt.easyxf(center_horiz_vert_text + black_border_text + gray_background_text + white_font)

    rotate_90_style = xlwt.easyxf(center_horiz_vert_text + black_border_text + rotate_90)
    default_style = xlwt.easyxf(center_horiz_vert_text + black_border_text + black_font)

    def put_white_box(self, ws, start: tuple, end: tuple, **kwargs):
        kwargs.setdefault("text", "-")
        style = self.rotate_90_style if kwargs.get("rotate_90") else self.default_style
        self.put_box(ws, start, end, style, **kwargs)

    @staticmethod
    def put_box(ws, start, end, style, **kwargs):
        style.font.bold = kwargs.get("bold", style.font.bold)
        style.font.height = kwargs.get("height", style.font.height)
        style.alignment.wrap = 1
        style.alignment.orie = kwargs.get("orientation", style.alignment.orie)

        ws.write_merge(start[1], end[1] - 1, start[0], end[0] - 1, kwargs.get("text"), style)


class Encounter:
    def __init__(self, start):
        self.start = start
        self.counter = start

    def add(self, delta):
        self.counter += delta
        return self.counter


class StaffExcelGenerator(ExcelHelperMixin):
    put_type_mapping = {
        "white": "put_white_box",
    }

    def add_color_palette(self):
        xlwt.add_palette_colour("gray_color", 0x21)
        self.wb.set_colour_RGB(0x21, 47, 117, 181)

    def __init__(self, queryset):
        self.queryset = queryset
        self.wb = xlwt.Workbook(style_compression=2)
        self.add_color_palette()

        self.ws = self.wb.add_sheet("1")

        self.ws.row(2).height_mismatch = True
        self.ws.row(2).height = 256 * 3

        i = Encounter(start=-1)
        self.ws.col(i.add(1)).width = 256 * 10  # No
        self.ws.col(i.add(1)).width = 256 * 10  # id
        self.ws.col(i.add(1)).width = 256 * 50  # full_name
        self.ws.col(i.add(1)).width = 256 * 30  # position
        self.ws.col(i.add(1)).width = 256 * 20  # create_at

    def save(self, name="contract.xls"):
        return self.wb.save(name)

    def generate_ws(self):
        Ey = Encounter(start=0)
        self.ws.write(Ey.counter, 1, "%(date)s sanasiga ko'ra holati" % {"date": timezone.now().date()})
        Ex = Encounter(0)
        Ey = Encounter(2)

        verbose_names_datas = [
            {"text": "N", "bold": True, "height": 190},
            {"text": "ID", "bold": True, "height": 190},
            {"text": "Full name", "bold": True, "height": 190},
            {"text": "Position", "bold": True, "height": 190},
            {"text": "Created at", "bold": True, "height": 190},
        ]
        for i in range(5):
            self.ws.write(Ey.counter, Ex.counter + i, verbose_names_datas[i]["text"], self.gray_style)
        Ex.counter = 0
        Ey.add(1)

        for i, staff in enumerate(self.queryset, start=1):
            self.write_box(self.ws, (Ex.counter, Ey.counter), (Ex.add(1), Ey.counter + 1), text=i)
            self.write_box(
                self.ws,
                (Ex.counter, Ey.counter),
                (Ex.add(1), Ey.counter + 1),
                text=staff.id,
            )
            self.write_box(
                self.ws,
                (Ex.counter, Ey.counter),
                (Ex.add(1), Ey.counter + 1),
                text=staff.title_sr,
            )
            self.write_box(
                self.ws,
                (Ex.counter, Ey.counter),
                (Ex.add(1), Ey.counter + 1),
                text=staff.position_sr,
            )
            self.write_box(
                self.ws,
                (Ex.counter, Ey.counter),
                (Ex.add(1), Ey.counter + 1),
                text=staff.created_at.strftime("%d.%m.%Y"),
            )

            Ey.add(1)
            Ex.counter = 0

    def write_box(self, *args, **kwargs):
        """Chooses box type based on participant status"""
        func = getattr(self, self.put_type_mapping.get("white"))
        func(*args, **kwargs)


class ImportExcelStaff(generics.GenericAPIView):
    def get(self, request):
        queryset = Staff.objects.all()
        excel = StaffExcelGenerator(queryset)
        excel.generate_ws()

        response = HttpResponse(content_type="application/ms-excel")
        response["Content-Disposition"] = 'attachment; filename="staff.xls"'
        excel.save(response)
        return response
