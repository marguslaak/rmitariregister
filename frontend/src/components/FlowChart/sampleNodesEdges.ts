import { edgeCommons } from 'utils/flowChart';
import sampleData from './sampleData.json';

export const initialNodes = sampleData
  .filter(
    (v, i, a) =>
      a.findIndex(v2 => v2.ariregistri_kood === v.ariregistri_kood) === i
  )
  .map(row => ({
    id: String(row.ariregistri_kood),
    data: { label: row.nimi },
    position: { x: 0, y: 0 },
  }));

export const initialEdges = sampleData
  .filter(row => !!row['osanikud.isikukood_registrikood'])
  .map(row => ({
    id: `e${row.ariregistri_kood}-${row['osanikud.isikukood_registrikood']}-${Math.random() * 1000}`,
    source: String(row.ariregistri_kood),
    target: String(row['osanikud.isikukood_registrikood']),
    label: `${row['osanikud.osaluse_suurus']} ${row['osanikud.osaluse_valuuta']}`,
    ...edgeCommons,
  }));
