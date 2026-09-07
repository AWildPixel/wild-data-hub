# ... [il tuo codice precedente per leggere i dati e preparare il dataframe] ...

    # COSTRUZIONE MAPPA
    fig = go.Figure()

    # Legenda avvicinata alla mappa (y=-0.05)
    colorbar_orizzontale = dict(
        orientation="h",
        y=-0.05,
        thickness=12,
        len=0.85,
        title=dict(text="Volume registrazioni", side="top"),
    )

    # Assicurati di mantenere all'interno di go.Choropleth i parametri dei tuoi dati
    fig.add_trace(go.Choropleth(
        # locations=tuo_dataframe['...'],
        # z=tuo_dataframe['...'],
        # ... (lascia intatti i parametri che avevi già qui dentro)
        colorbar=colorbar_orizzontale
    ))

    # Margine inferiore azzerato (b=0)
    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
            coastlinecolor="#4A4A4A",
            showland=True,
            landcolor="#E5E5E5",
            projection_type="natural earth",
        ),
        margin=dict(l=0, r=0, t=10, b=0),
    )

    st.plotly_chart(fig, use_container_width=True)

    # ... [il resto del tuo codice successivo] ...
