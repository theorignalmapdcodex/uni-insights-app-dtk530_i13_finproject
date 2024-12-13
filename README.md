# Heading Goes Here

This README provides guidance on using the Jupyter notebook `dtk530_i13_bb+llms.ipynb` for ...
## Table of Contents


# Things to Include
Include a link to my web app as well


# Map numeric cluster IDs to custom names
    data['Cluster'] = data['Cluster'].map({i: name for i, name in enumerate(cluster_names, start=1)})


            category_orders=category_orders,  # Custom order for clusters
        color_discrete_map=color_discrete_map  # Assign random colors



            # Updating legend appearance
    fig.update_layout(
        legend=dict(
            title="University Cluster Categories",  # Title for the legend
            font=dict(size=12),          # Legend font size
            itemsizing='constant',       # Consistent item sizing
            orientation='v'              # Vertical legend
        )
    )