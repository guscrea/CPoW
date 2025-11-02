from typing import Any
from transformers import pipeline
from transformers import AutoModelForSequenceClassification, AutoTokenizer
# note - local pylance recognizes libraries from venv file in project folder, 
# not .venv file in cpow folder. fix if you have chance.

def classify(sequence: str, printing=False,
             candidate_labels=["letter", "research paper", "presentation"]) -> tuple[str, Any]:
      """ classify document w/ one-shot model & given labels. 
      return tuple of top label & detailed results."""

      classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
      
      result = classifier(sequence, candidate_labels)
      scores = result["scores"]
      labels = result["labels"]
      scores = [round(float(score), 3) for score in scores]

      if printing==True:
         print(f"DOCUMENT PREVIEW: \n ...{sequence[400:1000]}... \n")
         print("REDICTIONS & CONFIDENCE:")
         for i in range(len(labels)):
             print(f"{labels[i]}: {scores[i]}")

      top_label = labels[
          scores.index(max(scores))
          ]
      
      return (top_label, result)


txt = """     RHODE ISLAND
       DEPARTMENT OF ENVIRONMENTAL MANAGEMENT
          OFFICE OF THE DIRECTOR
         235 Promenade Street, Room 425
         Providence, Rhode Island 02908


April 11, 2023
Chief
Office of Renewable Energy
Bureau of Ocean Energy Management
45600 Woodland Road
Sterling, Virginia 20166

RE:
Docket No. BOEM-2023-0011

Dear Chief of the Renewable Energy Office,

The Rhode Island Department of Environmental Management (RIDEM) supports offshore wind
energy development to mitigate the impacts of climate change and reduce greenhouse gas
emissions. The SouthCoast Wind Farm (formerly Mayflower Wind Farm) will provide the State
of Massachusetts with 1,204 MW of renewable energy through two power purchase agreements
but may have the capacity to supply an added 1,196 MW under additional power purchase
agreements. RIDEM is committed to ensuring that the local and regional environmental and
socioeconomic impacts of offshore wind development are minimized. As part of RIDEM’s effort
to enable offshore wind energy development while mitigating any adverse impacts, the agency
has reviewed the SouthCoast Wind Draft Environmental Impact Statement (DEIS), BOEM–
2023–0011.

The SouthCoast Wind Farm would be located in the area covered by Bureau of Ocean Energy
Management’s (BOEM’s) Renewable Energy Lease Number OCS-A 0521, approximately 20
nautical miles (nm) southeast Nantucket, Massachusetts and approximately 51 nm
southeast of the Rhode Island coast. The Project would comprise up to 149 positions in the
Leased Area to be occupied by up to 147 wind turbine generators and up to 5 offshore substation
platforms. The 149 positions will conform to a 1 nm x 1 nm grid layout with an east-west and
north-south orientation, consistent with the other lessees in the surrounding areas. The Project
would include two export cable corridors. One corridor would be used by multiple export cables
making landfall and interconnecting to the ISO New England Inc. grid in Falmouth,
2

Massachusetts. The other corridor would be used by multiple export cables making landfall and
interconnecting to the ISO New England Inc. grid at Brayton Point in Somerset, Massachusetts.
This second corridor will access Brayton Point via Rhode Island state waters through the
Sakonnet River.

The cable route is partially situated within the Rhode Island Coastal Resources Management
Council (CRMC) 2018 amended geographic location description (GLD 2018) approved by the
National Oceanic and Atmospheric Administration (NOAA) Office for Coastal Management on
December 7, 2018. As an applicant seeking a federal license or permit in federal waters within
the CRMC 2018 GLD, SouthCoast Wind must be consistent with the CRMC’s enforceable
policies, pursuant to 15 CFR Part 930, Subpart E.3.

The RIDEM has reviewed the SouthCoast Wind DEIS and offers the following comments to the
BOEM regarding the project. Comments include a review of relevant literature and staff
perspectives for further consideration in guiding impact assessments, as well as those relating to
the DEIS itself.

General Comments

Alternatives:
• The geographic area analysis for the analysis does not include adjacent leases. Therefore,
prospective effects the area of interest has on adjacent areas and vice versa are not
considered. This notion follows a similar concern of not evaluating the cumulative effects of
development on these areas.
• As presented, it seems the ‘No Action’ Alternative assumes a scenario where this project
does not move forward, but that all others in the Planned Activities Scenario would. As
stated in RIDEM’s previous projects’ DEIS comments, this seems unrealistic and may distort
one’s interpretation of potential impacts from this individual project. As a result, such a
scenario may imply that the impacts of this project specifically could be negligible, which
would not be accurate.

RIDEM suggestions for BOEM on requirements for the developer:
• Work with the Rhode Island commercial and recreational fishing industries to minimize
impacts to fishing activities and the biological resources on which they rely to the greatest
extent possible and offer appropriate mitigation plans if adverse impacts cannot be avoided.
o Mitigation plans should be developed with substantial input from the Rhode Island
Fishermen’s Advisory Board (FAB) and the CRMC.
• Conduct comprehensive fisheries resource monitoring surveys consistent with the
recommendations outlined by the Responsible Offshore Science Alliance (ROSA):
3

https://www.rosascience.org/wp-content/uploads/2022/09/ROSA-Offshore-Wind-Project-
Montioring-Framework-and-Guidelines.pdf.
o These surveys should address concerns related to biological impacts associated with
pile driving and operational noise, habitat loss and creation, sedimentation,
electromagnetic fields, and cumulative impacts.
o Surveys should include as many years as possible for data collection during pre,
during, and post construction phases of the project to best characterize the
environmental impacts.
o Given that one of the proposed cable routes is slated to pass through Rhode Island
state waters through the Sakonnet River, surveys should be designed to assess
impacts of the project to species of concern for Rhode Island, including species of
ecological importance, as well as social value.
 The RIDEM Division of Marine Fisheries is available to provide input to the
developer and contractors on proposed survey designs in federal and state
waters.
• Conduct high resolution benthic habitat characterization and avoid areas of sensitive benthic
habitats. Complex benthic habitats provide refuge and structure for juvenile fish and
invertebrates, as well as spawning areas for adult life history stages.
o The NOAA Greater Atlantic Regional Fisheries Office recently developed benthic
habitat mapping recommendations to better inform Essential Fish Habitat
consultations: https://media.fisheries.noaa.gov/2021-
03/March292021_NMFS_Habitat_Mapping_Recommendations.pdf?null. These
recommendations should be followed to ensure avoidance of sensitive habitats.
• Support NOAA’s efforts to minimize impacts to, or adapt, fish, invertebrate, and marine
mammal monitoring surveys in and around the wind energy area, as well as along the cable
route. These surveys provide some of the primary data used for informed fisheries and
wildlife management decisions, and disruptions to such long-term monitoring efforts will
introduce additional uncertainty into stock assessments and population monitoring. These
assessments are the primary tools used to manage and protect the resources, of which have
direct effects on commercial and recreational fishing.
• Minimize impacts to birds, sea turtles, and marine mammals, especially the critically
endangered North Atlantic right whale (Eubalaena glacialis).
o Southern New England has been identified as a significant foraging ground for right
whales during their migrations. Significant measures have been taken to improve their
population status via commercial lobster fishing restrictions. Additional commercial
fishing measures are being evaluated by the Atlantic Large Whale Take Reduction
Team, in addition to vessel speed requirement, to meet additional risk reduction
targets. As such, the project should take the necessary actions to ensure it does not
counteract these efforts.
4

o Impact minimization could occur through, but is not limited to, construction time of
year restrictions and exclusion zones, vessel speed restrictions (applied to all vessels
associated with the wind farm), and noise mitigation measures. Sound scientific data
collection and monitoring of the wind energy area is also essential to evaluating
potential effects in real-time to enable implementation of adaptive management
measures.
• The RIDEM Division of Fish and Wildlife prohibits any in-stream work from March 1 to
July 1 to protect the in-migration of anadromous species including alewife (Alosa
pseudoharengus), blueback herring (Alosa aestivalis), and American shad (Alosa
sapidissima). While the project does not include work instream, construction along the export
cable corridor has the potential to affect fish staging to enter the riverine systems during their
migration. The Division of Fish and Wildlife recommends that work through this corridor
does not take place from February 15 through July 1 to allow the anadromous migrations to
take place unimpeded. The Division also limits in-stream work during juvenile out-
migrations from September 15 until November 15. However, if the project can demonstrate
there will be no entrapment or entrainment of juvenile out-migrants, the Division may
reconsider its restrictions during state application review.

Project design
• The DEM is supportive of a 1 x 1 NM turbine grid layout to improve safety and fishing
ability of the windfarm as best as possible.
• For the HVAC and HVDC cables to be installed in federal and states’ waters, efforts should
be made to avoid not achieving target burial depth to minimize impacts to fishing activities
within the cable route. If a cable cannot be buried to 4 feet at minimum, or is located at a
crossing with existing cables, and mattressing is installed, all cable mattress locations should
be made available to the public and mattressing should be designed to limit the creation of
new fishing ‘hangs.’
• The minimum number of turbines and offshore service platforms to meet the project purpose
and need should be approved to minimize impacts to marine habitats and existing ocean uses
within the lease area. However, it is unclear in the project description what size wind turbine
generators (WTG) are expected to be used. In previous DEIS reviews, a range of WTG sizes
(MW specifically) has been presented. That information is not offered here, but based on the
proposed purpose and need of 2,400 MW and the number of available foundation locations
within the 1 x 1 NM grid, turbines larger than 16 MW are needed. Turbine size information
is critical when reviewing specific turbine location impacts to benthic habitats or species of
concern, as dropping certain locations may be necessary to mitigate environmental impacts.
• In the summary of project envelope design parameters, it is stated that the offshore service
platforms could remove up to 10 million gallons per day of once-through non-contact cooling
water, with a maximum intake velocity of 0.5 foot per second, with a maximum anticipated
temperature change of 18°F (10°C) from ambient water, and a maximum end-of-pipe
5

discharge temperature of 90°F (32.2°C). Is this the maximum scenario, where five offshore
service platforms (converter stations) are needed or does each OSP use this daily volume?
This section would benefit from some clarification and explanation about why additional
OSPs may be needed (e.g., are additional OSPs needed for specific amounts of additional
energy generation or is it a function of grid interconnection?).

DEIS Section-Specific Comments

Chapter 3 Affected Environment and Environmental Consequences

All aspects of the cable installation in Rhode Island state waters will undergo a thorough review
through the state permitting process for these activities. The Sakonnet River supports EFH for a
variety of fish species and has HAPCs for summer flounder and Atlantic Cod. As such, potential
seafloor disturbance, sediment suspension, boulder relocation, and deposition in Rhode Island
state waters from the cable installation will all be reviewed in great detail through the RIDEM
permitting process for a Water Quality Certification (RIGL § 46-12-3 and 250-RICR-150-05-1.1
et seq. – federal authority delegated to the State pursuant the Clean Water Act [CWA], 33 U.S.C.
§§ 1341-1342) and a Dredge Permit (pursuant to the Rules and Regulations for Dredging and the
Management of Dredged Materials - 250-RICR-150-05-2.1 et seq.).

The RIDEM is supportive of the SouthCoast Wind Farm and remains committed to minimizing
all potential impacts to fish habitat, especially within the Sakonnet River portion of Narragansett
Bay.
• The DMF monitors fish and invertebrate abundance in the Sakonnet River and Mt. Hope
Bay and has three surveys regularly sampling near the proposed cable route:
o Coastal Trawl Survey (http://www.dem.ri.gov/programs/marine-fisheries/surveys-
pubs/coastal-trawl.php)
o Narragansett Bay Seine (http://www.dem.ri.gov/programs/marine-
fisheries/surveys-pubs/narrabay-seine.php)
o Rhode Island Lobster Ventless Trap Survey
(http://www.dem.ri.gov/programs/marine-fisheries/surveys-pubs/lobster-
ventless.php)
o Please refer to the hyperlinked websites for survey methodologies.
• The seine survey samples at fixed locations from May – October annually, with a focus
on juvenile fish (Figure 1). The trawl survey samples at fixed stations on a monthly basis
year-round, in addition to seasonal random sampling throughout RI state waters.
o Refer to Figures 2-13 for mean annual abundance from the two surveys for
Atlantic cod, black sea bass, summer flounder (fluke), scup, tautog, and winter
flounder.
6

o Both Atlantic cod (Figures 2-3) and black sea bass (Figures 4-5) demonstrate
recent increases in overall relative abundance; while fluke (Figures 6-7), scup
(Figures 8-9) and tautog (Figures 10-11) remain variable. Winter flounder has
been consistently in decline (Figures 12-13).
• The Rhode Island Lobster Ventless Trap survey has documented high catch per trap (or
catch per unit effort) of lobsters in some years where the Sakonnet River has been
selected for randomized sampling (Figure 14).
• The Sakonnet River also supports a substantial commercial harvest of whelk (both
channeled and knobbed) (Figure 15).
• According to the NOAA Fisheries EFH mapper (available at
https://www.habitat.noaa.gov/apps/efhmapper/?page=page_3), the Sakonnet River is
documented as:
o Juvenile Atlantic cod Habitat Area of Particular Concern (HAPC) under the New
England Fishery Management Council’s Omnibus Essential Fish Habitat
Amendment 2
o Summer flounder HAPC (due to submerged aquatic vegetation) by the Mid-
Atlantic Fishery Management council
o Essential Fish Habitat (EFH) for the following 28 species’ life history stages:
Species
Eggs
Larvae
Juvenile
Adult
Neonate
Atlantic sea scallop
X
X
X
X

Winter flounder
X
X
X
X

Little skate


X
X

Atlantic herring

X
X
X

Atlantic cod
X
X
X
X

Pollock


X


Red hake
X
X
X
X

Silver hake
X
X

X

Yellowtail flounder


X
X

Windowpane flounder
X
X
X
X

Winter skate


X
X

Ocean pout
X

X


Albacore tuna


X


Bluefin tuna


X


Skipjack tuna



X

White shark




X
Yellowfin tuna


X


Smoothhound shark complex


X
X
X
Sand tiger shark


X

X
Scup
X
X
X
X

Longfin inshore squid
X

X
X

Atlantic mackerel
X
X
X
X

Bluefish


X
X

Atlantic butterfish
X
X
X
X

Spiny dogfish*


X (female)
X (male)

Atlantic Surfclam



X

Summer flounder

X
X
X

Black sea bass


X
X

7

 The DEIS incorrectly states that the Sakonnet River supports EFH for only
16 species.
• Given the presence of high-value habitat to many managed species, and HAPC for
Atlantic cod, avoidance of essential fish habitat will be a priority for all cable laying
activities.
• Furthermore, a detailed analysis of potential impacts to all life history stages of Atlantic
cod and winter flounder are not currently but should be included in the Final EIS.
o Narragansett Bay has been identified as a settlement and nursery area for early
stages of Atlantic cod until late spring temperatures increase. Southern New
England Atlantic cod numbers appear to be increasing but may be limited due to
warming water temperatures (Langan et al. 2020). Due to this project and others
that may be permitted in Atlantic cod EFH, minimizing impacts to Atlantic cod
nursery grounds like Narragansett Bay is critical.
o While winter flounder have been in decline in recent years, Sakonnet River larval
densities have been some of the highest sampled in Narragansett Bay (McManus
et al. 2021). The DEIS states that winter flounder eggs are particularly sensitive to
sedimentation, as described by Berry et al., (2011). Further discussion on
potential impacts to winter flounder life history stages should be presented within
the document.

3.5.5 Finfish, Invertebrates, and Essential Fish Habitat

Construction and decommissioning of offshore wind farms may lead to loss of sediment and thus
certain habitats. During any construction, local water turbidity may increase, as suspended solids
and contaminants within the sediments may be mobilized and transported by prevailing water
movements.
• These mobilized sediments may also smother neighboring habitats of sessile species, as well
as the living organisms themselves (Gill 2005).
• Suspended sediment poses a threat to fish within the construction area, as it may physically
clog their gills and limit oxygen intake (Lake and Hinch 1999). Larval states are more
vulnerable than adult life history stages due to more limited mobility, as well as larger gills
and higher oxygen consumption in proportion to body size (Auld and Schubel 1978;
Partridge and Michael 2010).
• Sediment dispersal may also smother eggs and benthic suspension feeders by clogging the
feeding or respiratory apparatus. Some benthic epifauna and deep burrowing infauna may
also be unable to escape burial by displaced sediment. While sedimentation events are
generally brief, seabed communities may be greatly altered and take years to recover (Maurer
et al. 1986).
• The RODEO study of the benthic habitat changes at the BIWF documented heavy
colonization of the turbine structures by blue mussels three years post-construction,
8

demonstrating changes in the dominant biota. Black sea bass were found in large numbers
and appeared to benefit from added structure (Hutchison et al. 2020).
o The study also found that the BIWF did not demonstrate the same strong vertical
epifaunal zonation as observed on European farms. This may suggest that after three
years, the habitat is still in a successional state and additional monitoring is needed to
document the final successional stage (Hutchison et al. 2020). As such, longer benthic
assessments should be conducted on projects moving forward.
• Soft sediments are generally preferred for wind farm development, as hard substrates may
create challenges in turbine foundation and transmission cable installation.
o Grabowski et al. (2014) suggest that soft sediment habitats have an inherent ability to
recover more rapidly from anthropogenic impacts than other substrates. However,
Henriques et al. (2014) contend that this is not appropriate logic to develop such areas
due to the high number of affected species and possible consequences of impacts on
those species for ecosystem structure and function (Grabowski et al. 2014; Henriques
et al. 2014).
The construction phase is the most likely to have negative effects on fish and habitat. Of primary
concern is construction noise generated by pile driving operations. High sound levels can cause
hearing loss (threshold shifts), elicit stress, and alter behavior of fish. Impacts will vary by
species, as well as sound exposure (Popper et al. 2003).
• For Atlantic cod, noise of frequencies from 100-1000 hertz has been found to reduce
reproductive output (Sierra-Flores et al. 2015).
• Operational phase noise is not likely to cause permanent damage, but it may mask
communication in some fish species (Wahlberg and Westerberg 2005). This remains one
of the least studied areas of wind farm noise impacts (Mooney et al. 2020).
• In the context of anthropogenic noise, it is important to consider invertebrates separately
from vertebrates; invertebrates (e.g., mollusks) hear in a different manner than vertebrates
due to their nervous system structure and hearing organs. Their hearing organs,
statocysts, work by detecting particle motion instead of sound pressure (Stocker 2002).
o There may be negative impacts near the project, as de Soto et al. (2013) suggest
that even routine anthropogenic noise can decrease recruitment of scallop larvae
in wild stocks (Madsen et al. 2006).
o Jones et al. (2020) determined that longfin squid exhibited a startle response to
pile driving noise in a lab setting but they habituated quickly in the short term. 24
hours later, the squid were re-sensitized to the noise.

DC and AC cables should not be considered comparable when determining impacts, as fish may
perceive static and alternating magnetic fields differently (Rommel and McCleave 1973a).
• Various elasmobranchs (e.g. smooth dogfish and blue sharks) and teleost fish (sea
lamprey, American eels, and Atlantic salmon) are all thought to be able to sense electric
fields at low levels (Heyer et al. 1981; Kalmijn 1982; Rommel and McCleave 1973b).
9

However, it is presently unknown whether behavioral changes will result from detected
AC electromagnetic fields. Behavioral responses of American lobster and little skates
have been documented in response to DC electromagnetic fields emitted by two high-
voltage DC cables: increased foraging/exploratory behavior in skates, and a subtler
exploratory response in lobsters (Hutchison et al. 2018; Hutchison et al. 2020).
• The impacts of induced electromagnetic fields are expected to be greater for cartilaginous
fish because they use electromagnetic signals to detect their prey (Bailey et al. 2014; Gill
2005; Gill and Kimber 2005; Bergstrom et al. 2014).
• Other fish may also be affected by interference with their capacity to orient in relation to
the geomagnetic field, potentially disturbing fish migration patterns (Metcalf et al. 2015)
and ultimately disturbing their habitat.
• RIDEM’s Division of Marine Fisheries is conducting a study, funded by Revolution
Wind LLC, on the Revolution Wind HVAC cables to be installed within Rhode Island
state waters (Narragansett Bay’s West Passage). Findings from this study will be
informative with respect to HVAC cable impacts on American lobster and Jonah crab.
However, additional studies will be needed in the Sakonnet River on the HVDC cables to
be installed as part of the SouthCoast Wind Farm to understand impacts to other species
from the DC cables.

The development may offer benefits to certain fish and invertebrate species through structure
creation (i.e., artificial reefs). The turbine foundations may increase hard substrate for
recruitment following any disturbance during the construction phase (Petersen and Malm 2006).
The reef effect can increase food availability (Degraer et al. 2020) and biodiversity and biomass
(Inger et al. 2009; Gill 2005; Linley et al. 2007). However, new habitat created by the turbine
foundations may not benefit all species that utilized the local habitat prior to construction and
may serve to attract biomass as opposed to result in increased ecosystem productivity. As such, it
is important that these elements be evaluated as possible throughout the project to best
understand the long-term effects of the region.

3.6.1 Commercial Fisheries and For-Hire Recreational Fishing

The developer has considered a variety of offshore fishing data sources: vessel trip reports
(VTRs), vessel monitoring systems, and Marine Recreational Information Program data. Each
data source has merits and limitations, as none of these data reporting systems were designed to
assess the spatial distribution and value of offshore catch. A variety of studies are currently
underway to generate additional data sharing systems and assessment tools.
• Other sources of data and improved methods should be incorporated into impact
assessment as they become available. For example, vessel monitoring system (VMS),
automatic identification system (AIS), and electronic monitoring data are becoming more
prevalent and may present opportunities to improve upon existing methods. These data
10

may offer higher spatial and temporal resolutions, and address challenges associated with
self-reporting, when compared to VTRs.
• Additional methods are particularly needed to understand potential changes to
recreational fishing activities.

The RIDEM looks forward to reviewing proposed fisheries resource monitoring survey designs
associated with the SouthCoast Farm. We recommend survey proposals should include a
preliminary power analysis demonstrating that the proposed design will achieve a minimum of
80% statistical power (see Cohen 1988). However, higher power levels, with low effect sizes
should be targeted. Both power and effect size should be discussed with the FAB prior to survey
implementation. Efforts should also be made to use shared sampling methods and results with
other wind development surveys and existing fisheries surveys.

The localized impacts from the construction and operation of the SouthCoast Wind Farm to
marine and avian organisms may be significant; however, this project will result in substantial
reduction of regional fossil fuel generation and lower emissions of nitrogen oxides and carbon
dioxide. Therefore, on balance, the RIDEM is supportive of the SouthCoast Wind Farm and its
contribution to mitigating the impacts of climate change.

The RIDEM is pleased to provide comments regarding the SouthCoast Wind Farm DEIS. Should
you have any questions regarding these comments, please feel free to contact Julia Livermore
(julia.livermore@dem.ri.gov; 401-423-1937).

Sincerely,


Jason McNamee, PhD
Deputy Director, RIDEM



11

References
André, M., et al., Low-frequency sounds induce acoustic trauma in cephalopods. Front. Ecol.
Environ. 9, 489– 493 (2011).
Auld, A.H., J. R. Schubel, Effects of suspended sediment on fish eggs and larvae: a laboratory
assessment. Estuar. Coast. Mar. Sci. 6, 153–164 (1978).
Bailey, H., K. L. Brookes, P. M. Thompson, Assessing environmental impacts of offshore wind
farms: lessons learned and recommendations for the future. Aquat. Biosyst. 10, 8 (2014).
Bergström, L., et al., Effects of offshore wind farms on marine wildlife—a generalized impact
assessment. Environ. Res. Lett. 9, 034012 (2014)
Berry, W. J., Rubinstein, N. I., Hinchey, E. K., Klein-MacPhee, G., and Clarke, D. G. 2011.
Assessment of dredging-induced sedimentation effects on winter flounder
(Pseudopleuronectes americanus) hatching success: results of laboratory investigations.
Bodznick, D., D. G. Preston, Physiological characterization of electroreceptors in the lampreys
Ichthyomyzon unicuspis and Petromyzon marinus. J. Comp. Physiol. 152, 209–217
(1983).
Brandt, M.J., A. Diederichs, K. Betke, G. Nehls, Responses of harbour porpoises to pile driving
at the Horns Rev II offshore wind farm in the Danish North Sea. Mar. Ecol. Prog. Ser.
421, 205–216 (2011).
Carey, D., Wilber, D., Read, L., Guarinello, M., Griffin, M., & Sabo, S. (2020). Effects of the
Block Island Wind Farm on Coastal Resources: Lessons Learned. Oceanography, 33(4),
70–81. https://doi.org/10.5670/oceanog.2020.407
Cohen J (1988) Statistical Power Analysis for the Behavioral Sciences. 2nd ed. Lawrence
Erlbaum Associates. https://doi.org/10.1016/C2013-0-10517-X
de Soto, N. A., et al., Anthropogenic noise causes body malformations and delays development
in marine larvae. Sci. Rep. 3, 2831 (2013).
Dean, M.J., W.S. Hoffman, and M.P. Armstrong. 2012. Disruption of an Atlantic cod spawning
aggregation resulting from the opening of a directed gill-net fishery. North American
Journal of Fisheries Management 32: 123–134.
DeCelles, G.R., Martins, D., Zemeckis, D.R., Cadrin, S.X. 2017. Using Fishermen’s Ecological
Knowledge to map Atlantic cod spawning grounds on Georges Bank. ICES Journal of
Marine Science. doi:10.1093/icesjms/fsx031
Degraer, S., Carey, D., Coolen, J., Hutchison, Z., Kerckhof, F., Rumes, B., & Vanaverbeke, J.
(2020). Offshore Wind Farm Artificial Reefs Affect Ecosystem Structure and
Functioning: A Synthesis. Oceanography, 33(4), 48–57.
https://doi.org/10.5670/oceanog.2020.405
Gill, A. B. Offshore renewable energy: ecological implications of generating electricity in the
coastal zone. J. Appl. Ecol. 42, 605–615 (2005).
Gill, A.B., J. A. Kimber, The potential for cooperative management of elasmobranchs and
offshore renewable energy development in UK waters. J. Mar. Biol. Assoc. U. K. 85,
1075–1081 (2005).
Grabowski, J.H., et al., Assessing the vulnerability of marine benthos to fishing gear impacts.
Rev. Fish. Sci. Aquac. 22, 142–155 (2014).
Henriques S., et al., Structural and functional trends indicate fishing pressure on marine
fish assemblages. J. Appl. Ecol. 51, 623–631 (2014).
Heyer, G. W., M. C. Fields, R. D. Fields, A. J. Kalmijn, in Biological Bulletin (MARINE
BIOLOGICAL LABORATORY 7 MBL ST, WOODS HOLE, MA 02543, 1981), vol.
12

13 161, pp. 344–345. 60. A. J. Kalmijn, Electric and magnetic field detection in
elasmobranch fishes. Science. 218, 916–918 (1982).
Hutchison, Z. L., Bartley, M. L., Degraer, S., English, P., Khan, A., Livermore, J., Rumes, B., &
King, J. W. (2020). OFFSHORE WIND ENERGY AND BENTHIC HABITAT
CHANGES: Lessons from Block Island Wind Farm. Oceanography, 33(4), 58–69.
Hutchison, Z. L., Gill, A. B., Sigray, P., He, H., & King, J. W. (2020). Anthropogenic
electromagnetic fields (EMF) influence the behaviour of bottom-dwelling marine species.
Scientific Reports, 10(1), 4219. https://doi.org/10.1038/s41598-020-60793-x
Hutchison, Z., A.B. Gill, P. Sigray, H. Haibo, J.W. King. Anthropogenic electromagnetic fields
(EMF) influence the behaviour of bottom-dwelling marine species. Scientific Reports.
10, 1-15 (2020).
Hutchison, Zoe et al., “Electromagnetic Field (EMF) Impacts on Elasmobranch (shark, rays, and
skates) and American Lobster Movement and Migration from Direct Current Cables”
(OCS BOEM OCS 2018-003, BOEM, 2018), p. 254.
Jones, I. T., Stanley, J. A., & Mooney, T. A. (2020). Impulsive pile driving noise elicits alarm
responses in squid (Doryteuthis pealeii). Marine Pollution Bulletin, 150, 110792.
https://doi.org/10.1016/j.marpolbul.2019.110792
https://www.intres.com/articles/meps2010/410/m410p177.pdf
Kritzer, J. 2020. Peer Review of the Atlantic Cod Stock Structure Working Group Report.
Presented to the NEFMC Scientific and Statistical Committee. June 4, 2020. Available at
https://s3.amazonaws.com/nefmc.org/Presentation-ACSSWG-Review-Panel-Report.pdf \
Lake, R. G., S. G. Hinch, Acute effects of suspended sediment angularity on juvenile coho
salmon (Oncorhynchus kisutch). Can. J. Fish. Aquat. Sci. 56, 862–867 (1999).
Langan, J., McManus, M.C., Zemeckis, D.R., Collie, J.S. 2019. Abundance and distribution of
Atlantic cod (Gadus morhua) in a warming southern New England. Fishery Bulletin.
118:2, 145-156.
Linley, E. A. S., T. A. Wilding, K. Black, A. J. S. Hawkins, S. Mangi, Review of the reef effects
of offshore wind farm structures and their potential for enhancement and mitigation. Rev.
Reef Eff. Offshore Wind Farm Struct. Their Potential Enhanc. Mitig. (2007).
Madsen, P.T., M. Wahlberg, J. Tougaard, K. Lucke, P. Tyack, Wind turbine underwater noise
and marine mammals: implications of current knowledge and data needs. Mar. Ecol.
Prog. Ser. 309, 279–295 (2006).
Maurer, D., et al., Vertical migration and mortality of marine benthos in dredged material: a
synthesis. Int. Rev. Gesamten Hydrobiol. Hydrogr. 71, 49–63 (1986).
Mavraki, N., Degraer, S., & Vanaverbeke, J. (2021). Offshore wind farms and the attraction–
production hypothesis: Insights from a combination of stomach content and stable isotope
analyses. Hydrobiologia. https://doi.org/10.1007/s10750-021-04553-6
McBride and Smedbol. 2020. An Interdisciplinary Review of Atlantic Cod (Gadus morhua)
Stock Structure in the Western North Atlantic Ocean. NOAA Technical Memorandum.
14 https://s3.amazonaws.com/nefmc.org/Interdisciplinary-Review-of-Atlantic-Cod-
StockStructure_200505_090723.pdf
McManus MC, Langan JA, Bell RJ, Collie JS, Klein-MacPhee G, Scherer MD, Balouskus RG
(2021) Spatiotemporal patterns in early life stage winter flounder Pseudopleuronectes
americanus highlight phenology changes and habitat dependencies. Mar Ecol Prog Ser
677:161-175. https://doi.org/10.3354/meps13857
Metcalfe, J., S. Wright, M. W. ever Pedersen, D. Sims, D. Righton, in ICES Annual Science
13

Conference 2015 (2015; http://orbit.dtu.dk/ws/files/119691328/Publishers_version.pdf).
NEFSC (Northeast Fisheries Science Center). 2017a. Georges Bank Atlantic cod. In Operational
assessment of 19 Northeast groundfish stocks, updated through 2016. NOAA, Natl. Mar.
Fish. Serv., Northeast Fish. Sci. Cent. Ref. Doc. 17-17, p. 38–46.
NEFSC (Northeast Fisheries Science Center). 2017b. Gulf of Maine Atlantic cod. In Operational
assessment of 19 Northeast groundfish stocks, updated through 2016. NOAA, Natl. Mar.
Fish. Serv., Northeast Fish. Sci. Cent. Ref. Doc. 17-17, p. 26–37.
NOAA, NOAA EFH Mapper (2018), (available at
https://www.habitat.noaa.gov/protection/efh/efhmapper/).
NOAA. 1999. Essential Fish Habitat Source Document: Atlantic Cod, Gadus morhua, Life
History and Habitat Characteristics. NOAA Technical Memorandum NMFS-NE-124.
https://repository.library.noaa.gov/view/noaa/3099
Öhman, M., P. Sigray, H. Westerberg, Offshore windmills and the effects of electromagnetic
fields on fish. AMBIO J. Hum. Environ. 36, 630–633 (2007).
Oviatt, C., S. Olsen, M. Andrews, J. Collie, T. Lynch, and K. Raposa. 2003. A century of fishing
and fish fluctuations in Narragansett Bay. Rev. Fish. Sci. 11:221–242.
Partridge, G.J., R. J. Michael, Direct and indirect effects of simulated calcareous dredge material
on eggs and larvae of pink snapper Pagrus auratus. J. Fish Biol. 77, 227–240 (2010).
Petersen, J. K., T. Malm, Offshore Windmill Farms: Threats to or Possibilities for the Marine
Environment. AMBIO J. Hum. Environ. 35, 75–80 (2006).
Popper, A. N., J. Fewtrell, M. E. Smith, R. D. McCauley, Anthropogenic Sound: Effects on the
Behavior and Physiology of Fishes. Mar. Technol. Soc. J. 37, 35–40 (2003).
Rommel, S. A., J. D. McCleave, Prediction of oceanic electric fields in relation to fish migration.
ICES J. Mar. Sci. 35, 27–31 (1973).
Rommel, S. A., J. D. McCleave, Sensitivity of American Eels (Anguilla rostrata) and Atlantic
Salmon (Salmo salar) to Weak Electric and Magnetic Fields. J. Fish. Res. Board Can. 30,
657–663 (1973).
Serchuk, F. M., and S. E. Wigley.1992. Assessment and management of the Georges Bank cod
fishery: an historical review and evaluation. J. Northwest Atl. Fish. Sci. 13:25–52.
Sheriff, J. 2018. Rhode Island cod fishing resurgence. Official News Magazine of the Rhode
Island Saltwater Anglers Association 239:16.
Sierra-Flores, R., T. Atack, H. Migaud, A. Davie, Stress response to anthropogenic noise in
Atlantic cod Gadus morhua L. Aquac. Eng. 67, 67–76 (2015).
Stocker, M., Fish, mollusks and other sea animals’ use of sound, and the impact of anthropogenic
noise in the marine acoustic environment. J. Acoust. Soc. Am. 112, 2431–2431 (2002).
Wahlberg, M., H. Westerberg, Hearing in fish and their reactions to sounds from offshore wind
farms. Mar. Ecol. Prog. Ser. 288, 295–309 (2005). 15
Zemeckis, D.R., C. Liu, G.W. Cowles, M.J. Dean, W.S. Hoffman, D. Martins, and S.X. Cadrin.
2017. Seasonal movements and connectivity of an Atlantic cod (Gadus morhua)
spawning component in the western Gulf of Maine. ICES Journal of Marine Science 74:
1780–1796.
Zemeckis, D.R., Martins, D., Kerr, L.A., Cadrin, S.X. 2014. Stock identification of Atlantic cod
(Gadus morhua) in US waters: an interdisciplinary approach. ICES Journal of Marine
Science 71(6): 1490-1506


14

Figures

Figure 1. RIDEM Narragansett Bay Seine fixed sampling stations. Refer to
http://www.dem.ri.gov/programs/marine-fisheries/surveys-pubs/narrabay-seine.php for additional survey details.
15


Figure 2. Trawl survey mean annual abundance of Atlantic cod from 2003 - 2020 for Sakonnet River stations



Figure 3. Mean annual abundance of Atlantic cod in Sakonnet River stations of the Narragansett Bay Seine survey
from 1988 – 2020
16


Figure 4. Trawl survey mean annual abundance of black sea bass from 1990 - 2021 for Sakonnet River stations


Figure 5. Mean annual abundance of black sea bass in Sakonnet River stations of the Narragansett Bay Seine survey
from 1988 - 2020
17


Figure 6. Trawl survey mean annual abundance of summer flounder (fluke) from 1990 - 2021 for Sakonnet River
stations



Figure 7. Mean annual abundance of summer flounder (fluke) in Sakonnet River stations of the Narragansett Bay
Seine survey from 1988 - 2020
18


Figure 8. Trawl survey mean annual abundance of scup from 1990 - 2021 for Sakonnet River stations



Figure 9. Mean annual abundance of scup in Sakonnet River stations of the Narragansett Bay Seine survey from
1988 – 2020
19


Figure 10. Trawl survey mean annual abundance of tautog from 1990 - 2021 for Sakonnet River stations


Figure 11. Mean annual abundance of tautog in Sakonnet River stations of the Narragansett Bay Seine survey from
1988 - 2020
20


Figure 12. Trawl survey mean annual abundance of winter flounder from 1990 - 2021 for Sakonnet River stations


Figure 13. Mean annual abundance of winter flounder in Sakonnet River stations of the Narragansett Bay Seine
survey from 1988 – 2020


21


Figure 14. Mean annual catch per trap in ventless traps of the Rhode Island lobster ventless trap survey for all
stations versus Sakonnet River stations only. Sampling in the Sakonnet does not occur every year due to the random
site selection design. Refer to http://www.dem.ri.gov/programs/marine-fisheries/surveys-pubs/lobster-ventless.php
for additional details.



Figure 15. Annual harvest of whelk from Sakonnet River tagging areas. Values aggregated for the following tagging
areas: 4A, 4B, 4C, 5, 5B, and 5C.  """

# testing:
top, _ = classify(txt, printing=True)
print(top)