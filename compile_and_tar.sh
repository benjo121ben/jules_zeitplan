#!/usr/bin/env sh
cargo leptos build --release &&
t_dir=jules_app &&
rm -r $t_dir
mkdir $t_dir &&
cp -r target/site/. $t_dir/site/ &&
cp requirements.txt $t_dir/requirements.txt &&
cp pull_zeitplan.py $t_dir/pull_zeitplan.py &&
# this was at some point necessary, might become relevant again who knows
# mv $t_dir/site/pkg/cp_red_char_sheet.wasm $t_dir/site/pkg/cp_red_char_sheet_bg.wasm &&
cp target/release/test-leptos $t_dir/test-leptos &&
cp Cargo_deploy.toml $t_dir/Cargo.toml && # cargo deploy sets site different
tar czf jules-app.tar.gz -C $t_dir . &&
echo project built and zipped into tar file
