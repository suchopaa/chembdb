create extension rdkit;
create table raw_data (id SERIAL,cid integer, smiles text);
insert into raw_data(cid, smiles) select ligand_id, smiles from ligand;
alter table raw_data add primary key (cid);
select * into mols from (select cid,mol_from_smiles(smiles::cstring) m from raw_data order by cid) tmp where m is not null;
create index molidx on mols using gist(m);
alter table mols add primary key (cid);
select cid,torsionbv_fp(m) as torsionbv,morganbv_fp(m) as mfp2,featmorganbv_fp(m) as ffp2 into fps from mols;
create index fps_ttbv_idx on fps using gist(torsionbv);
create index fps_mfp2_idx on fps using gist(mfp2);
create index fps_ffp2_idx on fps using gist(ffp2);
alter table fps add primary key (cid);

create or replace function get_mfp2_neighbors2(smiles text) 
returns table(cid integer, m mol, similarity double precision) as 
$$ 
select cid,m,tanimoto_sml(morganbv_fp(mol_from_smiles($1::cstring)),mfp2) as similarity 
from fps join mols using (cid) 
order by morganbv_fp(mol_from_smiles($1::cstring))<%>mfp2; 
$$ language sql stable ;
