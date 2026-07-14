const C = 299_792_458;
const MIN_LOG = 3;
const MAX_LOG = 22;
const RTL_MIN_HZ = 500_000;
const RTL_MAX_HZ = 1_766_000_000;

const regions = [
  {
    name: "Radio waves",
    min: 1e3,
    max: 3e8,
    examples: "AM radio, FM broadcast, aircraft radio, NOAA weather radio",
    sensor: "Antenna + SDR receiver",
    color: "#335c81",
  },
  {
    name: "Microwaves",
    min: 3e8,
    max: 3e11,
    examples: "Wi-Fi, Bluetooth, microwave ovens, radar, ADS-B near 1090 MHz",
    sensor: "Antenna + microwave receiver",
    color: "#5b8e7d",
  },
  {
    name: "Infrared",
    min: 3e11,
    max: 4e14,
    examples: "Heat radiation, thermal cameras, remote controls",
    sensor: "IR photodiode, thermal camera, bolometer",
    color: "#d97706",
  },
  {
    name: "Visible light",
    min: 4e14,
    max: 7.9e14,
    examples: "Human vision, cameras, optical telescopes",
    sensor: "Camera, photodiode, spectrometer",
    color: "#22c55e",
  },
  {
    name: "Ultraviolet",
    min: 7.9e14,
    max: 3e16,
    examples: "Sunburn, UV lamps, fluorescence",
    sensor: "UV photodiode or UV sensor",
    color: "#6d28d9",
  },
  {
    name: "X-rays",
    min: 3e16,
    max: 3e19,
    examples: "Medical imaging, high-energy astronomy",
    sensor: "X-ray detector",
    color: "#b91c1c",
  },
  {
    name: "Gamma rays",
    min: 3e19,
    max: 1e22,
    examples: "Nuclear processes, cosmic events, radiation monitoring",
    sensor: "Scintillator, Geiger tube, gamma spectrometer",
    color: "#3f1d46",
  },
];

const namedMarks = [
  { label: "AM", hz: 1e6 },
  { label: "FM", hz: 1e8 },
  { label: "Wi-Fi", hz: 2.4e9 },
  { label: "NOAA", hz: 137e6 },
  { label: "Visible", hz: 5.5e14 },
  { label: "X-ray", hz: 1e18 },
];

const sensorBands = [
  {
    name: "Radio waves",
    min: 1e3,
    max: 3e8,
    frequencyRange: "1 kHz to 300 MHz in this tool",
    wavelengthRange: "300 km to 1 m",
    collector: "Wire antenna, loop, dipole, Yagi, discone, ferrite bar",
    detector: "Antenna current plus tuner and ADC. The RTL-SDR covers a useful part of this region.",
    buy: "RTL-SDR kit, telescopic dipole, later a NOAA V-dipole or small discone.",
    learning: "Resonance, wavelength, impedance, polarization, noise floor, overload.",
    safety: "Receive only. Strong nearby transmitters can overload the receiver.",
    color: "#335c81",
  },
  {
    name: "Microwaves",
    min: 3e8,
    max: 3e11,
    frequencyRange: "300 MHz to 300 GHz",
    wavelengthRange: "1 m to 1 mm",
    collector: "Short dipole, patch antenna, horn, dish, waveguide",
    detector: "Microwave receiver front end. RTL-SDR can observe low microwave signals like ADS-B at 1090 MHz.",
    buy: "ADS-B antenna, 1090 MHz filter/LNA, later a satellite LNB or microwave module.",
    learning: "Directional gain, line of sight, feed geometry, filters, low-noise amplification.",
    safety: "Avoid transmit experiments for now. High-power RF is a different project.",
    color: "#5b8e7d",
  },
  {
    name: "Infrared",
    min: 3e11,
    max: 4e14,
    frequencyRange: "300 GHz to 400 THz",
    wavelengthRange: "1 mm to 750 nm",
    collector: "IR lens, aperture, reflector, IR-pass filter",
    detector: "IR photodiode for near IR; thermopile, bolometer, or thermal array for heat.",
    buy: "Raspberry Pi Camera Module 3 NoIR, IR filters, MLX90640 thermal camera breakout.",
    learning: "Reflected near IR versus emitted thermal IR, emissivity, calibration, heat transfer.",
    safety: "Invisible IR sources can still be bright. Avoid staring into IR LEDs or lasers.",
    color: "#d97706",
  },
  {
    name: "Visible light",
    min: 4e14,
    max: 7.9e14,
    frequencyRange: "400 THz to 790 THz",
    wavelengthRange: "750 nm to 380 nm",
    collector: "Lens, telescope, microscope objective, diffraction grating",
    detector: "CMOS camera, color sensor, photodiode, small spectrometer.",
    buy: "Raspberry Pi Camera Module 3 or HQ Camera, lens, tripod, diffraction grating, AS7341 color sensor.",
    learning: "Exposure, pixel values, color filters, optics, calibration frames, spectroscopy.",
    safety: "Use solar filters for any Sun work. Camera sensors and eyes are easy to damage.",
    color: "#22c55e",
  },
  {
    name: "Ultraviolet",
    min: 7.9e14,
    max: 3e16,
    frequencyRange: "790 THz to 30 PHz",
    wavelengthRange: "380 nm to 10 nm",
    collector: "UV-transparent window, small aperture, UV filter",
    detector: "UV photodiode or UVA/UVB sensor. Many normal lenses and plastics block UV.",
    buy: "LTR390 UVA sensor first; later compare UV-blocking glass, acrylic, shade, and clouds.",
    learning: "Photon energy, material absorption, sensor spectral response, weather context.",
    safety: "Protect eyes and skin. Do not experiment with UVC sources.",
    color: "#6d28d9",
  },
  {
    name: "X-rays",
    min: 3e16,
    max: 3e19,
    frequencyRange: "30 PHz to 30 EHz",
    wavelengthRange: "10 nm to 10 pm",
    collector: "No normal wire antenna. Use shielding, collimation, and detector material.",
    detector: "Scintillator plus photodiode/SiPM, Geiger tube, or semiconductor detector.",
    buy: "Passive radiation detector or dosimeter only after a safety plan. No X-ray source.",
    learning: "Ionization, shielding, counting statistics, background rate, dose units.",
    safety: "Do not buy, build, or operate X-ray sources for this learning project.",
    color: "#b91c1c",
  },
  {
    name: "Gamma rays",
    min: 3e19,
    max: 1e22,
    frequencyRange: "Above 30 EHz",
    wavelengthRange: "Below 10 pm",
    collector: "Detector volume matters more than antenna shape.",
    detector: "Geiger-Muller tube, scintillator crystal plus photodetector, or semiconductor detector.",
    buy: "Passive Geiger counter or calibrated dosimeter later, only for environmental background.",
    learning: "Discrete events, Poisson noise, integration time, shielding, false positives.",
    safety: "No radioactive sources. Passive background monitoring only.",
    color: "#3f1d46",
  },
];

const slider = document.querySelector("#frequencySlider");
const marker = document.querySelector("#spectrumMarker");
const sdrRange = document.querySelector("#sdrRange");
const frequencyReadout = document.querySelector("#frequencyReadout");
const wavelengthReadout = document.querySelector("#wavelengthReadout");
const regionReadout = document.querySelector("#regionReadout");
const exampleReadout = document.querySelector("#exampleReadout");
const logReadout = document.querySelector("#logReadout");
const sdrReadout = document.querySelector("#sdrReadout");
const periodReadout = document.querySelector("#periodReadout");
const sensorReadout = document.querySelector("#sensorReadout");
const canvas = document.querySelector("#waveCanvas");
const ctx = canvas.getContext("2d");
const tabButtons = document.querySelectorAll("[data-tab-target]");
const tabPanels = document.querySelectorAll("[role='tabpanel']");
const sensorSpectrumMap = document.querySelector("#sensorSpectrumMap");
const sensorCards = document.querySelector("#sensorCards");

function clamp(value, min, max) {
  return Math.min(max, Math.max(min, value));
}

function logToPercent(logValue) {
  return ((logValue - MIN_LOG) / (MAX_LOG - MIN_LOG)) * 100;
}

function hzToPercent(hz) {
  return logToPercent(Math.log10(hz));
}

function formatFrequency(hz) {
  const units = [
    ["YHz", 1e24],
    ["ZHz", 1e21],
    ["EHz", 1e18],
    ["PHz", 1e15],
    ["THz", 1e12],
    ["GHz", 1e9],
    ["MHz", 1e6],
    ["kHz", 1e3],
    ["Hz", 1],
  ];

  const [unit, factor] = units.find(([, unitFactor]) => hz >= unitFactor) || ["Hz", 1];
  const value = hz / factor;
  return `${formatNumber(value)} ${unit}`;
}

function formatLength(meters) {
  const units = [
    ["km", 1e3],
    ["m", 1],
    ["cm", 1e-2],
    ["mm", 1e-3],
    ["um", 1e-6],
    ["nm", 1e-9],
    ["pm", 1e-12],
    ["fm", 1e-15],
  ];

  const absolute = Math.abs(meters);
  const [unit, factor] = units.find(([, unitFactor]) => absolute >= unitFactor) || ["fm", 1e-15];
  return `${formatNumber(meters / factor)} ${unit}`;
}

function formatTime(seconds) {
  const units = [
    ["s", 1],
    ["ms", 1e-3],
    ["us", 1e-6],
    ["ns", 1e-9],
    ["ps", 1e-12],
    ["fs", 1e-15],
    ["as", 1e-18],
  ];

  const absolute = Math.abs(seconds);
  const [unit, factor] = units.find(([, unitFactor]) => absolute >= unitFactor) || ["as", 1e-18];
  return `${formatNumber(seconds / factor)} ${unit}`;
}

function formatNumber(value) {
  const absolute = Math.abs(value);
  if (absolute >= 100) return value.toFixed(0);
  if (absolute >= 10) return value.toFixed(1);
  return value.toFixed(2);
}

function regionForFrequency(hz) {
  return regions.find((region) => hz >= region.min && hz < region.max) || regions[regions.length - 1];
}

function setupTabs() {
  tabButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const targetId = button.dataset.tabTarget;

      tabButtons.forEach((tabButton) => {
        const isSelected = tabButton === button;
        tabButton.classList.toggle("is-active", isSelected);
        tabButton.setAttribute("aria-selected", String(isSelected));
      });

      tabPanels.forEach((panel) => {
        const isTarget = panel.id === targetId;
        panel.classList.toggle("is-active", isTarget);
        panel.hidden = !isTarget;
      });
    });
  });
}

function definitionItem(term, description) {
  const item = document.createElement("div");
  const dt = document.createElement("dt");
  const dd = document.createElement("dd");
  dt.textContent = term;
  dd.textContent = description;
  item.append(dt, dd);
  return item;
}

function buildSensorMap() {
  if (!sensorSpectrumMap || !sensorCards) return;

  const mapRows = sensorBands.map((band) => {
    const row = document.createElement("article");
    row.className = "sensor-map-row";

    const label = document.createElement("div");
    label.className = "map-label";
    const name = document.createElement("strong");
    const range = document.createElement("span");
    name.textContent = band.name;
    range.textContent = band.frequencyRange;
    label.append(name, range);

    const track = document.createElement("div");
    track.className = "map-track";
    const rangeBar = document.createElement("span");
    rangeBar.className = "sensor-map-range";
    const left = clamp(hzToPercent(band.min), 0, 100);
    const right = clamp(hzToPercent(band.max), 0, 100);
    rangeBar.style.left = `${left}%`;
    rangeBar.style.width = `${Math.max(right - left, 0.35)}%`;
    rangeBar.style.background = band.color;
    track.append(rangeBar);

    const copy = document.createElement("div");
    copy.className = "map-copy";
    const collector = document.createElement("strong");
    const wavelength = document.createElement("span");
    collector.textContent = band.collector;
    wavelength.textContent = band.wavelengthRange;
    copy.append(collector, wavelength);

    row.append(label, track, copy);
    return row;
  });

  const cards = sensorBands.map((band) => {
    const card = document.createElement("article");
    card.className = "sensor-card";
    card.style.setProperty("--card-color", band.color);

    const title = document.createElement("h3");
    title.textContent = band.name;

    const range = document.createElement("p");
    range.className = "range-line";
    range.textContent = `${band.frequencyRange} | ${band.wavelengthRange}`;

    const dl = document.createElement("dl");
    dl.append(
      definitionItem("Collector", band.collector),
      definitionItem("Detector", band.detector),
      definitionItem("Buy later", band.buy),
      definitionItem("Learning goal", band.learning),
      definitionItem("Safety note", band.safety),
    );

    card.append(title, range, dl);
    return card;
  });

  sensorSpectrumMap.replaceChildren(...mapRows);
  sensorCards.replaceChildren(...cards);
}

function drawWaveform(hz, region) {
  const width = canvas.width;
  const height = canvas.height;
  const padding = 42;
  const centerY = height * 0.54;
  const amplitude = height * 0.22;
  const logValue = Math.log10(hz);
  const normalized = clamp((logValue - MIN_LOG) / (MAX_LOG - MIN_LOG), 0, 1);
  const cycles = 1.25 + normalized * 42;

  ctx.clearRect(0, 0, width, height);

  const background = ctx.createLinearGradient(0, 0, width, 0);
  background.addColorStop(0, "#f8fafc");
  background.addColorStop(1, "#eef6ff");
  ctx.fillStyle = background;
  ctx.fillRect(0, 0, width, height);

  ctx.strokeStyle = "#d9e1ea";
  ctx.lineWidth = 1;
  for (let i = 0; i <= 8; i += 1) {
    const x = padding + ((width - padding * 2) * i) / 8;
    ctx.beginPath();
    ctx.moveTo(x, padding);
    ctx.lineTo(x, height - padding);
    ctx.stroke();
  }

  ctx.strokeStyle = "#9aa8b6";
  ctx.lineWidth = 1.4;
  ctx.beginPath();
  ctx.moveTo(padding, centerY);
  ctx.lineTo(width - padding, centerY);
  ctx.stroke();

  ctx.strokeStyle = region.color;
  ctx.lineWidth = 4;
  ctx.beginPath();

  const left = padding;
  const right = width - padding;
  const drawableWidth = right - left;
  for (let x = 0; x <= drawableWidth; x += 2) {
    const t = x / drawableWidth;
    const envelope = 0.92 - 0.08 * Math.cos(2 * Math.PI * t);
    const y = centerY - Math.sin(2 * Math.PI * cycles * t) * amplitude * envelope;
    if (x === 0) ctx.moveTo(left + x, y);
    else ctx.lineTo(left + x, y);
  }
  ctx.stroke();

  ctx.fillStyle = "#172033";
  ctx.font = "700 24px Arial, sans-serif";
  ctx.fillText(`${region.name}: scaled waveform density`, padding, 36);

  ctx.font = "500 16px Arial, sans-serif";
  ctx.fillStyle = "#667085";
  ctx.fillText(`Actual frequency: ${formatFrequency(hz)}. Actual period: ${formatTime(1 / hz)}.`, padding, height - 22);

  ctx.fillStyle = "#344054";
  ctx.font = "700 13px Arial, sans-serif";
  namedMarks.forEach((mark) => {
    const x = padding + (hzToPercent(mark.hz) / 100) * drawableWidth;
    if (x < padding || x > width - padding) return;
    ctx.fillRect(x - 1, height - padding - 12, 2, 12);
    ctx.fillText(mark.label, x + 5, height - padding - 2);
  });
}

function updateSdrRange() {
  const start = hzToPercent(RTL_MIN_HZ);
  const end = hzToPercent(RTL_MAX_HZ);
  sdrRange.style.left = `${start}%`;
  sdrRange.style.width = `${end - start}%`;
}

function update() {
  const logValue = Number(slider.value);
  const hz = 10 ** logValue;
  const wavelength = C / hz;
  const region = regionForFrequency(hz);
  const inSdrRange = hz >= RTL_MIN_HZ && hz <= RTL_MAX_HZ;

  marker.style.left = `${logToPercent(logValue)}%`;
  frequencyReadout.textContent = formatFrequency(hz);
  wavelengthReadout.textContent = formatLength(wavelength);
  regionReadout.textContent = region.name;
  exampleReadout.textContent = region.examples;
  logReadout.textContent = logValue.toFixed(2);
  sdrReadout.textContent = inSdrRange
    ? "Inside RTL-SDR Blog V4 direct tuning range"
    : "Outside RTL-SDR direct range";
  periodReadout.textContent = formatTime(1 / hz);
  sensorReadout.textContent = region.sensor;

  document.documentElement.style.setProperty("--accent", region.color);
  drawWaveform(hz, region);
}

updateSdrRange();
setupTabs();
buildSensorMap();
slider.addEventListener("input", update);
window.addEventListener("resize", update);
update();
