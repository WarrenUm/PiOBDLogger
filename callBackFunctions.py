def get_speed(s):
    global speed
    if not s.is_null():
        # speed = int(s.value.magnitude) #for kph
        speed = int(s.value.magnitude * .060934)  # for mph


def get_fuel_rail_press(fp):
    global fuel_rail_press
    if not fp.is_null():
        fuel_rail_press = float(fp.value.magnitude) * .145038  # kp to psi


def get_intake_temp(it):
    global intake_temp
    if not it.is_null():
        intake_temp = int(int(it.value.magnitude) * 1.8 + 32)  # C to F


def get_afr(af):
    global afr
    if not af.is_null():
        afr = float(af.value.magnitude) * 14.64 # Convert to AFR for normal gasoline engines


def get_rpm(r):
    global rpm
    if not r.is_null():
        rpm = int(r.value.magnitude)


def get_load(l):
    global load
    if not l.is_null():
        load = int(l.value.magnitude)


def get_coolant_temp(ct):
    global coolant_temp
    if not ct.is_null():
        coolant_temp = int(int(ct.value.magnitude) * 1.8 + 32) # convert to F


def get_intake_press(ip):
    global intake_pressure
    if not ip.is_null():
        intake_pressure = float(ip.value.magnitude)


def get_baro_press(bp):
    global baro_pressure
    if not bp.is_null():
        baro_pressure = float(bp.value.magnitude)


def get_dtc(c):
    global codes
    if not c.is_null():
        codes = c.value


def get_timing_a(ta):
    global timing_advance
    if not ta.is_null():
        timing_advance = str(ta.value).replace("degree", "") # in degrees / remove text from val
        timing_advance = float(timing_advance)


def get_maf(m):
    global maf
    if not m.is_null():
        maf = str(m.value).replace("gps", "")  # grams / second / remove text from val
        maf = float(maf)


def get_o2(o):
    global o2_trim
    if not o.is_null():
        o2_trim = str(o.value).replace("percent", "")  # +/- 3 percent normal range - negative = rich, positive = lean
        o2_trim = float(o2_trim)
