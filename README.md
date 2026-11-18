# The World in One Day — Wednesday 18 November 2026

Entry for make.fun's `news-image-20261118`: sum up 18 November 2026's
world news in one image.

`news.png` is a newspaper front page for the day:

- **Lead:** Trump lands in Manila for Quad talks ahead of a China visit,
  as ASEAN and APEC summits crowd the week.
- **The Gulf:** the US strikes an IRGC missile site on Qeshm Island;
  Iran's drones hit a US radar system in Bahrain.
- **Ukraine:** Kyiv hits the Crimean bridge for a second day as Russia
  pounds Kyiv's crossings.
- **Weather:** Cyclone Akvan strengthens over the Bay of Bengal.
- **Also today:** Canada–China trade deals as Xi meets Carney, Britain
  sanctions Israeli settlement firms, Dhoni retires from the IPL to
  mentor Chennai, and Baidu's chief warns of an AI bubble ahead of APEC.

The four pictures are AI-generated illustrations of the reported events
(no text baked into the pictures); every word on the page is typeset
with `build_frontpage.py` (Pillow + DejaVu fonts) so the page stays
legible. The footer says so: pictures are illustrations of reported
events.

## Run

`main.py` (Python 3.13, stdlib only, no network) copies `news.png` to
`/output/entry.png`. It runs twice and writes the same bytes both times.

## License

MIT — see `LICENSE`.
