# Kecamatan Coordinates Automation

**Status**: Ready to run
**Total**: 7,215 kecamatan
**Estimated Time**: ~7 hours (3s per query)

## Progress Tracker

- [ ] Batch 1: 0-100 (Aceh)
- [ ] Batch 2: 100-200 (Sumatera Utara)
- [ ] Batch 3: 200-300
- [ ] ...
- [ ] Complete: 7,215/7,215

## How to Run

```bash
# Process in batches of 100
python3 scripts/process_kecamatan_batch.py --start 0 --end 100
```

## Output

- `datasets/kecamatan_with_coords.json` - Final database
- `datasets/coords_progress.json` - Progress tracking
