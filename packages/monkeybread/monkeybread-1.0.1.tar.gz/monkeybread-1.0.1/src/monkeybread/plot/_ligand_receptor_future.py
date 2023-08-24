subset_pairs = [
    ('CXCL9', 'FCGR2A'),
    ('CXCL9', 'CCR2'),
    ('CXCL9', 'CCR3'),
    ('CXCL9', 'CCR5'),
    ('CXCL9', 'CCR4'),
    ('CXCL9', 'CCR1'),
    ('CXCL9', 'CCR10'),
    ('CXCL9', 'CCR8'),
    ('CXCL9', 'CXCR1'),
    ('CXCL9', 'CXCR3'),
    ('CXCL9', 'CXCR6'),
    ('CXCL9', 'CCR6'),
    ('CXCL9', 'CXCR4'),
    ('CXCL9', 'CX3CR1'),
    ('CXCL9', 'CCR7'),
    ('CXCL9', 'XCR1'),
    ('CXCL9', 'CXCR5'),
    ('CXCL9', 'CXCR2'),
    ('IFNG', 'CXCL9'),
    ('IL23A', 'CXCL9'),
    ('IL12B', 'CXCL9'),
    ('TNF', 'CXCL10'),
    ('IFNG', 'CXCL10'),
    ('IL1B', 'CXCL10'),
    ('CXCL10', 'CCR2'),
    ('CXCL10', 'CCR3'),
    ('CXCL10', 'CCR5'),
    ('CXCL10', 'CCR4'),
    ('CXCL10', 'CCR1'),
    ('CXCL10', 'CCR10'),
    ('CXCL10', 'CCR8'),
    ('CXCL10', 'CXCR1'),
    ('CXCL10', 'CXCR3'),
    ('CXCL10', 'CXCR6'),
    ('CXCL10', 'CCR6'),
    ('CXCL10', 'CXCR4'),
    ('CXCL10', 'CX3CR1'),
    ('CXCL10', 'CCR7'),
    ('CXCL10', 'XCR1'),
    ('CXCL10', 'CXCR5'),
    ('CXCL10', 'CXCR2')
]

ct_1 = 'mono/mac'
ct_2 = 'CD4 T'



pairs_order = None
niche_to_res = {}
for niche in sorted(set(adata.obs['niche'])):
    print(f"Niche {niche}")
    # Subset data
    adata_niche = adata[adata.obs['niche'] == niche]

    # Ligand-receptor analysis
    sq.gr.ligrec(
        adata_niche, 
        cluster_key='Cell Type', 
        complex_policy='min',
        corr_method='fdr_bh',
        corr_axis='clusters',
        use_raw=False,
        numba_parallel=False
    )

    niche_to_res[niche] = adata_niche.uns['Cell Type_ligrec']
    
    

niche_to_pairs = {}
for niche in  sorted(set(adata.obs['niche'])):  
    if ct_1 not in niche_to_res[niche]['pvalues'].columns:
        continue
    if ct_2 not in niche_to_res[niche]['pvalues'][ct_1].columns:
        continue
        
    df = niche_to_res[niche]['pvalues'][ct_1].loc[:, [ct_2]]

    df = df.loc[df[ct_2] < 0.001]
    niche_to_pairs[niche] = list(df[ct_2].index)

subset_pairs = niche_to_pairs['6']
print("Total: ", subset_pairs)

da = {}
for niche in  sorted(set(adata.obs['niche'])):  
    if ct_1 not in niche_to_res[niche]['pvalues'].columns:
        continue
    if ct_2 not in niche_to_res[niche]['pvalues'][ct_1].columns:
        continue
        
    df = niche_to_res[niche]['pvalues'][ct_1].loc[:, [ct_2]]

    if pairs_order is None:
        pairs_order = sorted(df.index)

    #df = df.loc[pairs_order]

    df = df.loc[subset_pairs]

    da[niche] = list(df[ct_2])

df_plot = pd.DataFrame(
    data=da,
    index=subset_pairs
)
df_plot

fig, ax = plt.subplots(1,1,figsize=(4,10))
sns.heatmap(
    df_plot,
    cmap='viridis_r',
    mask=df_plot.isna(),
    #lw=0.05,
    #linecolor='black',
    ax=ax
)
#sns.heatmap(df_plot, cmap='viridis')
