from geopy.distance import geodesic

COMPANY_LAT = 10.194770122217097
COMPANY_LON = 106.37463117148687
MAX_DISTANCE = 100


def check_company_location(user_lat, user_lon):
    company = (
        COMPANY_LAT,
        COMPANY_LON
    )

    user = (
        user_lat,
        user_lon
    )

    distance = geodesic(
        company,
        user
    ).meters

    return distance <= MAX_DISTANCE, distance