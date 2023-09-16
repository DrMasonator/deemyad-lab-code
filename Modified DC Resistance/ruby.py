# Use this one
# Determined by Shen et al. 2020
def PressureRef(reference, TReference, measured, TMeasured) -> float:
    a = 1870.
    b = 5.63

    l0 = tempCorrection(reference, TReference)
    l1 = tempCorrection(measured, TMeasured)

    delta = l1 - l0

    return round(a * (delta / l0) * (1 + b * (delta / l0)), 2)


def Pressure(measured, reference=694.22) -> float:
    a = 1870.
    b = 5.63
    delta = measured - reference

    return round(a * (delta / reference) * (1 + b * (delta / reference)), 2)


# Determined by Datchi et al. 2007
def tempCorrection(R1, T):
    dt = T - 296

    if 296 <= T:
        delta = .00746 * dt - 3.01 * pow(10, -6) * pow(dt, 2) + 8.76 * pow(10, -9) * pow(dt, 3)

    elif 50 <= T < 296:
        delta = .00664 * dt + 6.77 * pow(10, -6) * pow(dt, 2) - 2.33 * pow(10, -8) * pow(dt, 3)

    elif T < 50:
        delta = - 0.887

    return R1 - delta


# Determined by Dorogokupets and Oganov 2007
def P2(reference, TReference, measured, TMeasured):
    a = 1884.
    b = 5.5

    l0 = tempCorrection(reference, TReference)
    l1 = tempCorrection(measured, TMeasured)

    delta = l1 - l0

    return a * (delta / l0) * (1 + b * (delta / l0))


# Determined by Shen et al. 2020 (Wikipedia)
def P3(reference, TReference, measured, TMeasured):
    a = 1870.
    b = 5.63

    l0 = tempCorrection(reference, TReference)
    l1 = tempCorrection(measured, TMeasured)

    return a / b * (pow(l1 / l0, b) - 1)


if __name__ == "__main__":
    print(Pressure(696.7, 694.3))