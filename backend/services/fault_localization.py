from network.models import Pole
from telemetry.models import Telemetry


def localize_fault():
    poles = Pole.objects.all().order_by("sequence_number")

    last_on = None
    first_off = None

    for pole in poles:
        latest = (
            Telemetry.objects.filter(device__pole=pole)
            .order_by("-timestamp")
            .first()
        )

        if latest is None:
            continue

        if latest.energized:
            last_on = pole
        else:
            first_off = pole
            break

    if last_on and first_off:
        print(f"Fault located between {last_on.pole_id} and {first_off.pole_id}")

        return {
            "start_pole": last_on,
            "end_pole": first_off,
            "confidence": 0.90,
        }

    print("No fault detected")
    return None