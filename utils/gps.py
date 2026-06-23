from geopy.distance import geodesic

# Tọa độ công ty của bạn
COMPANY_LAT = 10.194578458975384
COMPANY_LON = 106.37445664227818

# bán kính cho phép
MAX_DISTANCE = 80


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

    return (
        distance <= MAX_DISTANCE,
        distance
    )