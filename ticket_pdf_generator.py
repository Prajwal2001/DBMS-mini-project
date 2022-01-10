from PIL import Image, ImageDraw, ImageFont


def generate_ticket_pdf(ticket: dict):
    im = Image.open("./static/images/ticket_template.jpg")
    d = ImageDraw.Draw(im)

    pnr_loc = (210, 342)
    trainno_loc = (260, 430)
    trainname_loc = (750, 430)
    from_loc = (225, 518)
    to_loc = (670, 518)
    arr_time_loc = (285, 613)
    dept_time_loc = (317, 657)
    dept_date_loc = (790, 657)
    reach_time_loc = (307, 700)
    reach_date_loc = (780, 700)
    price_loc = (230, 774)
    booking_date_loc = (300, 849)

    text_color = (0, 0, 0)
    font = ImageFont.truetype("arial.ttf", 22)

    d.text(pnr_loc, str(ticket["pnr"]), fill=text_color, font=font)
    d.text(trainno_loc, str(ticket["train_no"]), fill=text_color, font=font)
    d.text(trainname_loc, str(
        ticket["train_name"]), fill=text_color, font=font)
    d.text(from_loc, str(ticket["from_station"]), fill=text_color, font=font)
    d.text(to_loc, str(ticket["to_station"]), fill=text_color, font=font)
    d.text(arr_time_loc, str(
        ticket["arrival_time"]), fill=text_color, font=font)
    d.text(dept_time_loc, str(
        ticket["depart_time"]), fill=text_color, font=font)
    d.text(dept_date_loc, str(
        ticket["travelling_date"]), fill=text_color, font=font)
    d.text(reach_time_loc, str(
        ticket["reaching_time"]), fill=text_color, font=font)
    d.text(reach_date_loc, str(
        ticket["reaching_date"]), fill=text_color, font=font)
    d.text(price_loc, str(ticket["price"]), fill=text_color, font=font)
    d.text(booking_date_loc, str(
        ticket["booking_date"]), fill=text_color, font=font)

    x1, x2, x3, y = 180, 480, 790, 1010
    for i in ticket["passengers"]:
        d.text((x1, y), str(i[0]), fill=text_color, font=font)
        d.text((x2, y), str(i[1]), fill=text_color, font=font)
        d.text((x3, y), str(i[2]), fill=text_color, font=font)
        y += 43

    fileName = "./tickets/ticket_pnr_" + str(ticket["pnr"]) + ".pdf"
    im.save(fileName)
    return fileName
