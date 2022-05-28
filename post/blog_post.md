# Building a custom ML pipeline from scratch

Cloud providers are offering hands-on services for creating pipelines for machine learning projects. These pipelines support all stages of the machine learning process, from data fetching, preparation and serving to model training, selection and evaluation, to model serving in a managed and monitored environment.
The hands-on offering is specifically well suited to train ML models for problems that the cloud providers are putting forward, such as text analysis, translation or image classification / segmentation.

But what about all the other types of problems where ML can be used? The applicability of a full-fledged ML pipeline that can recognise cats from dogs is limited for most data scientist / ml engineers / scientist, who are probably faced with slightly more complex issues, with hopefully more potential benefits.

At electricityMap, We have data about electricity around the world. A lot of that data in fact, which we organise to support multiple grid decarbonation use cases. Some of these use cases require robust forecasting model for power production. We'll use this setting here as a premise for what we really want to explore.
How can we build a full-fledged ML pipeline, that leverages some of the cloud services, for power production forecasting?

### The requirements

