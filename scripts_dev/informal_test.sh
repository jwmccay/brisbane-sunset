mkdir data_test
cp ../data/n37_w123_1arc_v3.tif data_test

echo ""
echo "Subset..."
sunset-subset-tif \
    -i "data_test/n37_w123_1arc_v3.tif" \
    -o "data_test/n37_w123_subset.tif" \
    -b 1900 900 400 400
ls data_test

echo ""
echo "Reproject..."
sunset-reproject-tif \
    -i data_test/n37_w123_subset.tif \
    -o data_test/n37_w123_subset_reproject.tif \
    -e 7131
ls data_test

echo ""
echo "Run..."
echo "Expect approx: \"Sunset at 4:09 on 1/18/2025\""
sunset-run -d "2025-1-18" -oc "37.6924344,-122.4150331" \
    -r "data_test/n37_w123_subset_reproject.tif" \
    -cm "xy" \
    -dp -fd "data_test/figs"

rm -r data_test