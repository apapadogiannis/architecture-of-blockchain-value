// Checks that the model code inside the demo page (docs/index.html) gives the same numbers as the
// Python module, by comparing it with the stored tables in outputs/.
// Usage: node scripts/check_demo.mjs        (run from anywhere; needs Node 18 or later, no packages)
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const html = readFileSync(join(root, "docs/index.html"), "utf8");
const block = html.match(/\/\/ MODEL-BEGIN[\s\S]*?\/\/ MODEL-END/);
if (!block) { console.error("model block not found in docs/index.html"); process.exit(1); }
const { benchmarkValue, complementarityShare, scalingLaw, unequalValue, splitValues } =
  new Function(block[0] + "\nreturn { benchmarkValue, complementarityShare, scalingLaw, unequalValue, splitValues };")();

const csv = name => readFileSync(join(root, "outputs", name), "utf8").trim().split("\n").slice(1);
const close = (a, b) => Math.abs(a - b) <= 1e-9 * Math.max(1, Math.abs(b));
let checked = 0, failed = 0;
const expect = (what, got, want) => { checked++; if (!close(got, want)) { failed++; console.error(`MISMATCH ${what}: page ${got}, stored ${want}`); } };

for (const line of csv("fig5_capability_scaling.csv")) {
  const [K, single, multi, meta] = line.split(",").map(Number);
  expect(`single K=${K}`, benchmarkValue(1, 0), single);
  expect(`multi K=${K}`, benchmarkValue(K, 0.5), multi);
  expect(`meta K=${K}`, benchmarkValue(K, 0.75), meta);
}
for (const line of csv("fig8_scaling_laws.csv")) {
  const [u, s, m, r] = line.split(",").map(Number);
  expect(`sarnoff u=${u}`, scalingLaw("sarnoff", u), s);
  expect(`metcalfe u=${u}`, scalingLaw("metcalfe", u), m);
  expect(`reed u=${u}`, scalingLaw("reed", u), r);
}
for (const line of csv("ext_unequal_values.csv")) {
  const [K, share, direct, bonus, V, bonusEq] = line.split(",").map(Number);
  const v = unequalValue(K, 0.75, share);
  expect(`unequal V K=${K} share=${share}`, v, V);
  expect(`unequal bonus K=${K} share=${share}`, v - K, bonus);
  expect(`equal bonus K=${K}`, benchmarkValue(K, 0.75) - K, bonusEq);
  expect(`split adds up K=${K} share=${share}`, splitValues(K, share).reduce((a, b) => a + b, 0), direct);
}
const text = Object.fromEntries(csv("text_numbers.csv").map(l => { const p = l.split(","); return [p[0], Number(p[p.length - 1])]; }));
const round6 = x => Number(x.toFixed(6));
expect("share multi K=50", round6(complementarityShare(50, 0.5)), text.fig5_share_from_complementarity_multi_K50);
expect("share meta K=50", round6(complementarityShare(50, 0.75)), text.fig5_share_from_complementarity_meta_K50);
expect("general phi, u, N", benchmarkValue(50, 0.75, 2, 3, 5), text.eq14_closed_form_meta_K50);

console.log(`demo page: ${checked} numbers compared with outputs/, ${failed} mismatches`);
process.exit(failed ? 1 : 0);
