import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

#config
current_url = "https://www.fandango.com/"
movie_name = "Avengers Endgame"
zip_code = "33323"
show_type = "Standard Showtimes"
movie_date = "2019-04-25"
timeout = 20
temp_theater_name = ""
temp_movie_time = ""
movies_links = []
image_names = []

start = time.time()


# chrome_options = Options()
#chrome_options.add_argument("--headless")
# chrome_options.add_argument("--start-maximized")

driver = webdriver.Safari()
driver.maximize_window()
driver.get(current_url)

#Search

search_field = driver.find_element_by_css_selector(".fan-input.style-search")
if search_field.is_displayed():
    search_field.clear()
    search_field.send_keys(movie_name)
    search_field.send_keys(Keys.RETURN)
else:
    print("search_field is not displayed")


element_present = EC.visibility_of_element_located((By.CSS_SELECTOR, 'section#movies'))
WebDriverWait(driver, timeout).until(element_present)

#Click Movie Times of the right movie

movie_results = driver.find_elements_by_css_selector("section#movies ul li")
for movie in movie_results:
    if "Cast + Crew" in movie.get_attribute("innerHTML"):
        link = movie.find_element_by_css_selector(".results-detail .movie-info-details .btn.btn-showtimes.btn-ticket").get_attribute("href")
        link = link + "?date=" + movie_date
        driver.get(link)
        break


element_present = EC.visibility_of_element_located((By.CSS_SELECTOR, '.date-picker__location-input.js-date-input'))
WebDriverWait(driver, timeout).until(element_present)

#zip_code
zip_field = driver.find_element_by_css_selector(".date-picker__location-input.js-date-input")
if zip_field.is_displayed():
    zip_field.clear()
    zip_field.send_keys(zip_code)
    zip_field.send_keys(Keys.RETURN)
    zip_field.clear()
else:
    print("zip_code is not displayed")

#so that it waits for the zip to be changed
time.sleep(2)

element_present = EC.visibility_of_element_located((By.CSS_SELECTOR, 'section.pagination'))
WebDriverWait(driver, timeout).until(element_present)

page_count = int(driver.find_element_by_css_selector("section.pagination :nth-last-child(2)").get_attribute("innerHTML"))

for current_page in range(page_count):
    current_page = current_page+1
    element_present = EC.visibility_of_element_located((By.CSS_SELECTOR, '.theater__wrap'))
    WebDriverWait(driver, timeout).until(element_present)
    theaters = driver.find_elements_by_css_selector(".theater__wrap")
    for theater in theaters:
        #Get theater name
        temp_theater_name =  theater.find_element_by_css_selector(".theater__name .color-light").get_attribute("innerHTML")

        showtimes = theater.find_elements_by_css_selector("ul.theater__showtimes.font-sans-serif-alt")
        result_showtimes = ""
        for showtime in showtimes:
            if show_type in showtime.get_attribute("innerHTML"):
                result_showtimes = showtime
                break
        if result_showtimes == "":
            break
        avaliable_times = result_showtimes.find_elements_by_css_selector("ol li")
        #check if it's reserved seating
        try:
            result_showtimes.find_element_by_css_selector(".icon-amenity-reserved-seating")
        except:
            print()
            print("No reserved seating for " + temp_theater_name)
            print()
            break
        for timeslot in avaliable_times:

            #timeslot
            try:
                temp_movie_time = timeslot.find_element_by_tag_name("a").get_attribute('innerHTML')
            except NoSuchElementException:
                # print(timeslot.screenshot("temp_movie_time"+str(current_page)+".png"))
                continue

            image_names.append(temp_theater_name + " - " + temp_movie_time)

            #link
            try:
                link = timeslot.find_element_by_css_selector("a.btn.showtime-btn.showtime-btn--available").get_attribute('href')
            except NoSuchElementException:
                # print(timeslot.screenshot("timeslot"+str(current_page)+".png"))
                continue

            movies_links.append(link)
    if current_page < page_count:
        #go next
        driver.find_element_by_css_selector("section.pagination :last-child").click()

driver.close()

#start dowloading
driver = webdriver.Safari()
driver.maximize_window()
for i in range(len(movies_links)):
    driver.get(movies_links[i])

    try:
        element_present = EC.visibility_of_element_located((By.ID, 'AreaRepeater_TicketRepeater_0_quantityddl_0'))
        WebDriverWait(driver, timeout).until(element_present)
        dropdown = Select(driver.find_element_by_id("AreaRepeater_TicketRepeater_0_quantityddl_0"))
        dropdown.select_by_value('1')
        button = driver.find_element_by_id("NewCustomerCheckoutButton")
        button.click()

        element_present = EC.visibility_of_element_located((By.CSS_SELECTOR, '.standard'))
        WebDriverWait(driver, timeout).until(element_present)

        #Print the image if it has good seats
        avaliable_seats = driver.find_elements_by_css_selector(".standard.availableSeat")
        for seat in avaliable_seats:
            #left 200 and less than 390 | top 206 and less than 494
            left = float(seat.value_of_css_property("left")[:-2])
            top = float(seat.value_of_css_property("top")[:-2])
            if left > 220.0 and left < 370.0 and top > 216.0 and top < 484.0:
                driver.find_element_by_id("map").screenshot(image_names[i] + ".png")
                break
    except:
        print("Showtime Full: " + movies_links[i])

driver.close()

end = time.time()

print( str(int((end - start)/60)) + ":" + str(int((end - start) % 60)))
