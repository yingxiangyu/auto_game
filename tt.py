import utils

games = utils.new_set_game_pos()
image = games[0].get_window_img()
for i in utils.ocr(image):
    print(i)
