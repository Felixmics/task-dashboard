# Bathymetry Void-Fill Data Sources — Cairns Region GBR

Compiled 2026-11-21 from public data portals. Maps to voids in depth_source_coverage_PD_Fitzroy_v4.png.

## Existing 8 sources (v4 priority map)

| Pri | Source | Res | Type |
|-----|--------|-----|------|
| 1 | AHO Reference Surface | 0.5–1 m | MEASURED |
| 2 | IN2022_V07 EM2040c | 2 m | MEASURED |
| 3 | CSIRO EM300 regrids | 5 m | MEASURED |
| 4 | Multibeam 10 m (EM300 + RV Inv) | 10 m | MEASURED |
| 5 | Elvis lidar | 5 m | MEASURED |
| 6 | Satellite-derived (GBR10/EOMAP) | 10 m | MODELLED |
| 7 | 16 m multibeam (Falkor/NGBR/Michaelmas) | 16 m | MEASURED |
| 8 | GBR30 | 35 m | MODELLED |

## Where the voids are

The v4 map shows three main void types in the Port Douglas–Fitzroy corridor:

1. **Mid-shelf gaps** — areas between inner-shelf lidar (pri 5) and outer-shelf multibeam tracks (pri 2–4), currently falling back to satellite-derived (pri 6) or GBR30 (pri 8)
2. **Inter-reef channels** — passages between reefs where no survey vessel has run a track, often 30–60 m depth
3. **Outer-shelf slope** — beyond the reef matrix where only GBR30 or coarser compilations exist

## Void-fill candidates — BATHYMETRY

### Tier A — Could upgrade existing voids to MEASURED or higher-res

| Dataset | Res | Portal | What it fills |
|---------|-----|--------|---------------|
| **IN2016_V05 GBR Bathymetry** | 10–210 m | data.csiro.au/collection/csiro:58347 (sister record) | Earlier CSIRO voyage — may cover tracks NOT in IN2022_V07. Check overlap; any non-overlapping tracks fill mid-shelf gaps at 10 m measured |
| **AusSeabed individual survey acquisitions** | varies (2–76 m) | portal.ga.gov.au/persona/marine | The portal indexes every contributed multibeam survey. Turn on "Survey Acquisitions" layer, zoom to Cairns shelf — any track not in your v4 map is a void filler. Free download per survey |
| **ELVIS lidar orders (new coverage)** | 1–5 m | elevation.fsdf.org.au | Queensland adds new coastal lidar captures regularly. Order the footprint layer, compare against your pri-5 Elvis extent — any new capture in the PD–Fitzroy corridor extends measured coverage inshore. Qld LiDAR >3 yrs old is free. 1 m and 3 m bathymetry DEMs available |
| **Queensland LiDAR coverage footprint** | — | data.qld.gov.au/dataset/queensland-lidar-data-lidar-coverage | Shows EXACTLY where Qld lidar exists. Download this shapefile and overlay on HD9 to find measured lidar you're missing |
| **Deepreef.org airborne lidar** | ~2–5 m | deepreef.org | Airborne lidar covers ~2/3 of GBR reefs. Focus: reef tops and shallow flanks. Any reef in your corridor not in your pri-5 coverage could be here |

### Tier B — Compilation grids (fill gaps at coarser resolution)

| Dataset | Res | Portal | What it fills |
|---------|-----|--------|---------------|
| **AusBathyTopo GBR 30 m 2017** | 30 m | ecat.ga.gov.au record 0f4e635c-... | Same base data as your GBR30 (pri 8) but the GA version — may include source surveys your GBR30 clip missed. Download and diff |
| **gbr100** | 100 m | catalogue.eatlas.org.au record 200aba6b-... | eAtlas high-res compilation. COARSER than GBR30 so won't improve resolution, but useful as a cross-check and for the outer-shelf slope beyond GBR30 extent |
| **GA High-resolution depth model** | 100 m | ecat.ga.gov.au record 5c47b141-... | GA's own 100 m GBR compilation — same coverage story as gbr100 |
| **AusBathyTopo 250 m (2026)** | 250 m | portal.ga.gov.au | National scale, too coarse for fishing but fills absolute voids on the outer slope |
| **GEBCO 2021** | ~450 m | gebco.net | Global fallback — only useful beyond the continental shelf where nothing else exists |
| **Copernicus coastal sat-derived bathy** | varies | data.marine.copernicus.eu product BATHYMETRY_GLO_PHY_COASTAL_L4_MY_016_001 | Global coastal satellite bathymetry — compare against your pri-6 sat-derived extent, may cover different areas |

### Tier C — NOT usable (data bans / restrictions)

| Dataset | Why excluded |
|---------|-------------|
| HI220 LADS | Not releasable |
| AHO ENC Online | Not allowed |
| GBR30 (sharing) | Personal use only, not cleared to share |
| EM122 | Out |
| SS2013_T03 official-box clip | Out |

## Void-fill candidates — OCEANOGRAPHIC (pelagic engine layers)

These don't fill depth voids but fill the PELAGIC scoring layers (SST, chlorophyll, currents) that the engine uses.

| Dataset | Variable | Res | Portal | Use in RODNEY |
|---------|----------|-----|--------|---------------|
| **IMOS OceanCurrent** | Surface currents, sea level anomaly | ~10 km | oceancurrent.aodn.org.au | Gridded altimetry-derived currents — feeds flood/ebb layer, current arrows on HD9 |
| **IMOS SRS-SST (GHRSST)** | SST | 0.02° (~2 km) | portal.aodn.org.au | Daily satellite SST for the GBR — feeds SST gradient layer, pelagic engine temperature breaks |
| **Copernicus Marine GLOBAL_ANALYSISFORECAST_PHY** | Currents, temp, salinity | 0.083° (~9 km) | data.marine.copernicus.eu | Global ocean physics forecast — backup current/temp feed, free registration |
| **Copernicus Marine GLOBAL_ANALYSISFORECAST_BGC** | Chlorophyll, plankton, nutrients | 0.25° (~28 km) | data.marine.copernicus.eu | Biogeochemistry forecast — chlorophyll edge detection for pelagic engine |
| **Copernicus OCEANCOLOUR_GLO_BGC_L3** | Chlorophyll-a (satellite) | ~4 km | data.marine.copernicus.eu | Satellite ocean colour — observed chl-a, sharper than model, good for colour breaks |
| **eReefs (AIMS)** | Currents, temp, chl, sediment, nutrients | ~1 km (GBR4) ~4 km | ereefs.aims.gov.au | GBR-SPECIFIC hydrodynamic + biogeochemical model. Best available for reef-scale currents and water quality. Daily output |

## Skill-sourced additions (Claude skills library, 2026-11-21)

Sources extracted from 8 loaded GBR-specific skills. These skills are older reference material — endpoints, datum values, and workflow details may be outdated. Treat as leads to investigate, not hard rules.

### Bathymetry — specific products and endpoints

| Dataset | Res | Endpoint / Record | Skill source | What it fills |
|---------|-----|-------------------|-------------|---------------|
| **AusSeabed WCS (GBR 30m numeric)** | 30 m | `warehouse.ausseabed.gov.au/geoserver/ows` — WCS 2.0.1, coverage IDs: `ausseabed__AusBathyTopo__Great_Barrier_Reef__Bathymetry_B_30m_2017_OV` (tile B, 16–23S) and `_A_` (10–17S). Float32 elevation, negative=depth, nodata -9999. SCALEFACTOR=0.1 gives ~0.003° grid (~4.6 MB corridor clip). CC BY 4.0 | upwellings | Direct WCS download of GBR30 corridor subset — avoids the 3.5 GB zip. Use `_OV` suffix (numeric); `_HS` is hillshade (uint8), not data |
| **Port Douglas–Fitzroy 16 m MSL 2020** | 16 m | GA record 149720 | when-where-why-marks | Specific GA product covering the PD–Fitzroy corridor at 16 m measured resolution. Fills mid-shelf gaps between lidar and deep multibeam. MSL vertical datum |
| **IN2022 + SS200809 10 m grids** | 10 m | CSIRO (specific survey products) | wonky-hole-detection | Individual 10 m multibeam survey grids used for wonky hole detection. Cross-validate against GBR30 |

### Habitat and benthic classification

| Dataset | Type | Endpoint | Skill source | Use in RODNEY |
|---------|------|----------|-------------|---------------|
| **Allen Coral Atlas** (benthic) | Vector WFS | `allencoralatlas.org` — layer `coral-atlas:benthic_data_verbose`. Classes: Sand, Rubble, Rock, Coral/Algae, Seagrass, Microalgal Mats. CC BY 4.0, free, no auth | gbr-env-scan | Dense corridor-wide benthic substrate. Drives bait-holding classification. No `startIndex` paging — tile the bbox (6×6 grid) instead |
| **Allen Coral Atlas** (geomorphic) | Vector WFS | `allencoralatlas.org` — layer `coral-atlas:geomorphic_data_verbose`. Classes: Deep Lagoon, Shallow Lagoon, Plateau, Reef Flat, Reef Crest, Reef Slope, **Back Reef Slope**, Patch Reefs, Drowned Reef, etc. CC BY 4.0 | gbr-env-scan | Geomorphic classification to ~15 m depth. CQL_FILTER and bbox are mutually exclusive — combine into single `CQL_FILTER=class_name='X' AND BBOX(geom,W,S,E,N)` |
| **CCMR benthic layer** | Raster | eAtlas / CSIRO | wonky-hole-detection | Benthic classification used alongside ACA for reef masking in wonky hole detection |
| **eAtlas WFS — GBRMPA reef features** | Vector WFS | `maps.eatlas.org.au/maps/wfs?service=WFS&version=1.0.0&request=GetFeature&typeName=ea-be:GBR_GBRMPA_GBR-features&outputFormat=application/json&bbox=145.75,-17.05,146.55,-16.30&maxFeatures=800` (EPSG:4283) | when-where-why-marks | Reef boundary polygons for proximity scoring. Place marks on their GBRMPA reef polygon |
| **BRUVS data (AIMS eAtlas)** | Point CSV | eAtlas catalogue — 233 drops for Cairns corridor | gbr-env-scan | Ground-truth for benthic/species validation. Evidence layer MC16 |
| **eAtlas GeoNetwork catalogue** | Discovery | `catalogue.eatlas.org.au/geonetwork/srv/eng/catalog.search` | gbr-env-scan | Master catalogue for GBR datasets — search `bathymetry cairns`, `benthic`, `sediment`, `reef features` |

### Oceanographic feeds — specific endpoints and dataset IDs

| Dataset | Variable | Endpoint / Dataset ID | Skill source | Use in RODNEY |
|---------|----------|----------------------|-------------|---------------|
| **NOAA ERDDAP MUR SST** | SST | `jplMURSST41` — griddap, `analysed_sst[(last-7):1:(last)]`, lat/lon stride 2 = 0.02°, CSV. Lags ~1–2 days | upwellings | Daily gap-filled SST for thermal front detection. Free, no auth |
| **NOAA ERDDAP VIIRS Chl-a** | Chlorophyll-a | `nesdisVHNnoaaSNPPnoaa20NRTchlaGapfilledDaily` — `chlor_a[(last)][(0.0)]`, lat/lon stride 4, latitude ascending | upwellings | Near-real-time chlorophyll for colour break reading. Cloud-blanked — use 3-day composites |
| **Open-Meteo Marine API** | Currents, sea level | `open-meteo.com` — ocean_current_velocity (km/h), ocean_current_direction (toward), sea_level_height_msl. 0.1° grid, past_days=1 + forecast_days=3, max 50 pts/request, cell_selection=sea | upwellings | Current velocity and direction for upwelling lift scoring. Free, no auth. Can time out — retry with backoff |
| **Open-Meteo Forecast** | Wind | `api.open-meteo.com` — wind in knots, 3 points, past 5 + forecast 3 days | upwellings | Wind for Ekman transport modifier in upwelling score |
| **NOAA Coral Reef Watch 5km SST** | SST, SST anomaly | `coralreefwatch.noaa.gov/product/5km/index_5km_sst.php` | gbr-env-scan | Reef-scale SST and anomaly patterns. Cross-check against ERDDAP MUR |
| **NASA PACE/OCI (Worldview)** | Chlorophyll-a L2 | `worldview.earthdata.nasa.gov` — add "Chlorophyll a (L2) — PACE / OCI" layer | gbr-env-scan | Satellite chlorophyll for live colour break detection. Compare against eAtlas climatology |
| **eReefs GBR4 Hydro v2.0** | SST, salinity, currents, sea level, wind | NCI THREDDS OPeNDAP: `.../dodsC/fx3/gbr4_v2/gbr4_simple_<YYYY-MM>.nc` | ereefs-integration | GBR-specific 4 km hydrodynamic model. **BLOCKED from cloud** — use on Mick's PC or via AIMS WMS |
| **eReefs GBR1 Hydro (1 km)** | SST, currents | NCI THREDDS | ereefs-integration | Higher-res 1 km version. Shorter temporal coverage. **BLOCKED** |
| **eReefs GBR4 BGC** | Chl-a, turbidity, nutrients | NCI THREDDS — vars: Chl_a_sum, Kd_490, NO3, NH4, TSS | ereefs-integration | Biogeochemistry model — depth-resolved chl-a. Fills cloud gaps. **BLOCKED** |
| **AIMS THREDDS aggregation** | All eReefs | `thredds.ereefs.aims.gov.au/thredds/catalog.html` | ereefs-integration | Aggregated daily/monthly means. WMS for visual; OPeNDAP for extraction. **403 from cloud** |
| **BOM tidal predictions** | Tide heights, times | `bom.gov.au/australia/tides/` — Cairns port | when-where-why-conditions | Preferred tide source for locked depth rule |
| **BOM marine forecast** | Wind, seas, swell | `bom.gov.au/qld/forecasts/cairns.shtml` (marine tab) | gbr-env-scan | Wind/sea go/no-go. **BOM blocks automation** — Mick checks manually |
| **seatemperature.org** | Coastal SST | `seatemperature.org/australia/queensland/cairns.htm` | gbr-env-scan | Quick coastal SST cross-check |

### Blocked hosts (cannot fetch from cloud workspace)

| Host | Error | Alternative |
|------|-------|-------------|
| `services.ga.gov.au` REST | 403 | Use AusSeabed WCS at `warehouse.ausseabed.gov.au` instead |
| `gbr-dms.aims.gov.au` | Proxy denied | Use eAtlas catalogue or AIMS THREDDS WMS |
| `dapds00.nci.org.au` (NCI THREDDS) | Blocked | Run eReefs extraction on Mick's PC; use AIMS WMS for visual |
| `thredds.ereefs.aims.gov.au` | 403 | WMS may work for display layers; OPeNDAP blocked |

### Datum note (from skills — CORRECTED by Drive REEF_TIDE_OFFSETS.md)

**Two MSL numbers — do not mix up:**
- **1.74 m = Cairns wharf MSL above LAT** (Maritime Safety Queensland 2026 tidal planes, station 100280)
- **~1.53–1.57 m = reef MSL above LAT** (varies by station — see reef tide offset table below)
- **1.55 m = locked project figure** — matches the reefs, NOT the wharf

Anything saying "MSL = LAT + 1.74" applied to a reef is the wharf figure and must be corrected to the reef value from the station table. AHD = LAT + 1.643 m. GA 30 m grid and 16 m products are about MSL. Chartplotter and sounder are LAT.

## Google Drive–sourced additions (2026-11-21)

Sources extracted from Mick's Google Drive folders ("claude file store", "Claude working model files", "Database Grok Organized", "Grok Data base marine"). These are older reference material — treat as leads, not hard rules.

### Reef tide offset table (from REEF_TIDE_OFFSETS.md — LOCKED, authoritative)

Tide at a reef ≠ Cairns tide. Formula: tide_at_reef = local_MSL + range_ratio × Cairns_anomaly(t − time_diff).

| Station | dt (min) | MSL above LAT (m) | Range ratio |
|---------|----------|-------------------|-------------|
| Cairns | 0 | 1.74 | 1.00 |
| Palm Cove | −8 | 1.71 | 1.00 |
| Green Island | −6 | 1.54 | 1.00 |
| Fitzroy Island | −9 | 1.57 | 1.00 |
| Sudbury Cay | −6 | 1.57 | 1.00 |
| High Island | −6 | 1.63 | 0.95 |
| Michaelmas Cay | −11 | 1.56 | 0.91 |
| Saxon Reef | −14 | 1.53 | 0.88 |
| Low Islets | 0 | 1.59 | 0.93 |
| Russell Island | −17 | 1.48 | 1.00 |

Source: MSQ Semidiurnal Tidal Planes 2026 (epoch 2010–2029). Positions between stations use inverse-distance blend of 3 nearest. dt = time difference (negative = earlier than Cairns). Cairns model: 16-constituent harmonic fit, RMS 0.076 m vs official 2026 CSV (52,560 readings). Label: MODEL reef tide (official MSQ offsets), not BOM.

Existing code: `tide_reef.py` (Drive folder "Reef tide layer 10 November 2026", id `1ZuIPQysUOe2GryuXB7XJufWjKQaui9Q9`) — 20-reef, 10-day, 10-min series using live MSQ CKAN predictions as backbone. JavaScript twin embedded in planner v66 artifact.

### Additional bathymetry products (from mapping_sources_v3, 225 rows)

| Dataset | Res | CRS | Status | Drive source |
|---------|-----|-----|--------|-------------|
| **GBR10/EOMAP SDB** | 9.6 m | EPSG:4326 | Held | Shallow (<~20 m) reef tops only. MSL datum |
| **S2 log-ratio pseudo-SDB** | 9.6 m | EPSG:4326 | Held | Sentinel-2 B02/B03 relative depth (not calibrated). 671 MB |
| **sdb_cairns.tif** | 10 m | EPSG:32755 | Held | Cairns SDB raster, 138 MB, covers whole corridor bbox |
| **SOI Falkor multibeam 16 m** | 16 m | — | Held | 3 surveys: fk200429, fk200802, fk200930 (Drive IDs in Data Coverage Ref) |
| **AusBathyTopo 250 m** (multiple vintages) | 250–267 m | EPSG:32755/4326 | Held | Corridor clips already in Drive. Vintage order: 2026 GA151280, 2024 GA150050, 2023 GA148758, 2009 GA67703 |
| **NGBR 16 m corridor clip** | 15.4 m | EPSG:32755 | Held | Confirmed covering corridor. Footprint 16.45–17.05°S, 145.40–146.40°E (smaller than full engine corridor) |
| **Working depth grid** | 32.1 m | EPSG:32755 | Held | `registry_RODNEY-working-depth-0-to-100m_32.1m_2026_EPSG32755_cog.tif` (27 MB, in Database Grok Organized) |

### Additional habitat and evidence layers (from Cairns Reef Data Library)

| Dataset | Type | Portal / Link | Use in RODNEY |
|---------|------|---------------|---------------|
| **Reef Cover: Cairns-Cooktown** | Vector (237 reefs, 15 m geomorphic + benthic) | PANGAEA 925657 | Validated reef zonation with field calibration (160 transects, 23 reefs). CC BY 4.0 |
| **Allen Coral Atlas 15 m bathymetry** | Raster DEM | allencoralatlas.org | Third DEM in multiscale set — fills shallow reef voids |
| **Multiscale bathy + terrain vars** (Guillaume et al.) | Raster | DOI 10.25845/ggyv-pq15 (AIMS), DOI 10.5061/dryad.wdbrv15vk (14 GB, 23 reefs) | Ready-made multiscale DEMs and derived terrain variables |
| **GBR Seabed Biodiversity** | Point data (1,210 sites) | ResearchData Australia record 681787 | 9 substrate classes, 26 biohabitat classes, 12 faunal groups. Towed video + BRUVS. NOT YET DOWNLOADED |
| **MARS marine sediment database** | Point data | marine.ga.gov.au | GA sediment samples. NOT YET OPENED |
| **Seamap Australia** | WMS/WFS | seamapaustralia.org, GeoServer at geoserver.imas.utas.edu.au | National benthic habitat layer, hierarchical classification. Includes GBR10 |
| **Shallow Marine Mask** (NESP MaC 3.17) | Shapefile | eAtlas share (IN DRIVE, Medium-Low version) | Shallow seabed where hard bottom and old shorelines are likely |
| **GA inter-reef sediments report** | PDF (212 pp) | IN DRIVE (GA10248) | Comprehensive inter-reef sediment characterisation |

### Additional oceanographic sources (from Cairns Reef Data Library)

| Dataset | Variable | Portal | Use in RODNEY |
|---------|----------|--------|---------------|
| **Sentinel-3B OLCI true colour** | True colour WMS | CSIRO GeoServer WMS: `www.cmar.csiro.au/geoserver/ereefs/Sentinel-3B-OLCI-GBR/wms` | 2019-04 to ~2026-05 (6 months behind). Visual water colour for turbidity/colour break reading |
| **NASA GIBS** | True colour, chl, SST | earthdata.nasa.gov GIBS API | The only layers current to the day. MODIS, VIIRS true colour and chl, GHRSST MUR SST |
| **eReefs Data Broker API** | All eReefs | data.ereefs.org.au | Open, no key. Alternative to THREDDS |
| **eReefs extraction tool** | CSV output | extraction.ereefs.aims.gov.au | AIMS point extraction service for eReefs variables |

### QGIS rendering reference (from bathyvision_fixed_wcs.py)

Reusable depth colour ramp for chartplotter-style rendering:

| Depth | Colour | Label |
|-------|--------|-------|
| 0 m | #1ae8ff | Intertidal / Reef Flat |
| −5 m | #00a2d9 | 0–5 m Shallow |
| −20 m | #004fa8 | 5–20 m Slope |
| −50 m | #011640 | 20–50 m Drop-off |
| −200 m | #0b0114 | Deep Channels |

Method: dual hillshade (East 90°, z=2.5, opacity 0.45 + NW 315°, z=1.5, opacity 0.35) over pseudocolour depth, with 2 m smoothed contours. CRS: EPSG:7855 (GDA2020 MGA Zone 55). Note: WCS URL `ga.gov.au` in the script is broken from cloud; use `warehouse.ausseabed.gov.au` instead.

### Still open (from Data Coverage Reference addition, 6 Nov 2026)

1. Backscatter grids (CSIRO) — still not held
2. NGBR 16 m corridor clip footprint (16.45–17.05°S) is smaller than the full engine corridor (15.9–17.3°S)
3. Vertical datum and cell size need recording per layer in the register

## Recommended actions (priority order)

1. **Download Qld LiDAR coverage shapefile** from data.qld.gov.au — overlay on HD9 to identify measured lidar that's not in pri-5. Free, immediate.

2. **Browse AusSeabed portal** at portal.ga.gov.au/persona/marine — turn on Survey Acquisitions layer, zoom to 16°S–17.5°S, 145.5°E–146.5°E. Any track line not in your v4 map = free measured data to download.

3. **Order new ELVIS lidar** for any new coastal captures since your last order — check elevation.fsdf.org.au, free if >3 years old.

4. **Grab IN2016_V05** from CSIRO — the earlier northern GBR voyage. Any non-overlapping track with IN2022_V07 gives you 10 m measured data in a current void.

5. **Set up eReefs feed** for the pelagic engine — 1 km resolution GBR-specific currents and chlorophyll, purpose-built for this reef. Freely accessible via AIMS THREDDS.

6. **Register for Copernicus Marine** — free account gives daily SST and ocean colour downloads for the GBR box. Better than any other source for pelagic water features.
