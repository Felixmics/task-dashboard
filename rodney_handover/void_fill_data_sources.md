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

## Recommended actions (priority order)

1. **Download Qld LiDAR coverage shapefile** from data.qld.gov.au — overlay on HD9 to identify measured lidar that's not in pri-5. Free, immediate.

2. **Browse AusSeabed portal** at portal.ga.gov.au/persona/marine — turn on Survey Acquisitions layer, zoom to 16°S–17.5°S, 145.5°E–146.5°E. Any track line not in your v4 map = free measured data to download.

3. **Order new ELVIS lidar** for any new coastal captures since your last order — check elevation.fsdf.org.au, free if >3 years old.

4. **Grab IN2016_V05** from CSIRO — the earlier northern GBR voyage. Any non-overlapping track with IN2022_V07 gives you 10 m measured data in a current void.

5. **Set up eReefs feed** for the pelagic engine — 1 km resolution GBR-specific currents and chlorophyll, purpose-built for this reef. Freely accessible via AIMS THREDDS.

6. **Register for Copernicus Marine** — free account gives daily SST and ocean colour downloads for the GBR box. Better than any other source for pelagic water features.
