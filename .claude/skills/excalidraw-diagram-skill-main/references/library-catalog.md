# Excalidraw Community Library Catalog

Curated list of the most useful libraries from [excalidraw-libraries](https://github.com/excalidraw/excalidraw-libraries). Use `library_helper.py` to fetch items on demand.

---

## Cloud & Infrastructure

| Library | Source Path | Notable Items | Complexity |
|---------|-------------|---------------|------------|
| AWS Architecture Icons | `octo-kumo/aws-architecture-icons.excalidrawlib` | EC2, S3, Lambda, RDS, VPC, CloudFront, DynamoDB, API Gateway, ECS, SQS, SNS | Complex |
| AWS Simple Icons | `morbidick/aws.excalidrawlib` | Lambda, S3, EC2, RDS, DynamoDB | Simple |
| Azure Architecture | `tomengan/azure.excalidrawlib` | App Service, Functions, SQL DB, Storage, VNet, AKS, Cosmos DB | Complex |
| Azure Icons | `psensei/azure-icons.excalidrawlib` | VM, App Gateway, Key Vault, Monitor, DevOps | Medium |
| Azure Cloud Design | `jbadge/cloud-design-patterns.excalidrawlib` | Load Balancer, Cache, Queue, Gateway patterns | Medium |
| Azure Integration | `dwightlossern/azure-integration.excalidrawlib` | Logic Apps, Service Bus, API Management, Event Grid | Medium |
| Azure IoT | `dwightlossern/azure-iot.excalidrawlib` | IoT Hub, Digital Twins, Stream Analytics | Medium |
| Google Cloud Icons | `alixhami/gcp.excalidrawlib` | Compute Engine, Cloud Run, BigQuery, GKE, Cloud Storage, Pub/Sub | Medium |
| GCP Additional | `pomdtr/gcp.excalidrawlib` | Cloud Functions, Firestore, Spanner, Memorystore | Medium |

## System Design & Architecture

| Library | Source Path | Notable Items | Complexity |
|---------|-------------|---------------|------------|
| System Design | `rohanp/system-design.excalidrawlib` | Server, Database, Load Balancer, CDN, Cache, Message Queue, Client | Medium |
| C4 Model | `psensei/c4-model-v2.excalidrawlib` | Person, Software System, Container, Component, Relationship | Medium |
| Software Architecture | `seren5240/software-architecture.excalidrawlib` | Microservice, API, Database, Message Broker, Gateway | Medium |
| Hexagonal Architecture | `zhorben/hexagonal-architecture.excalidrawlib` | Port, Adapter, Domain, Application Core | Simple |

## Networking

| Library | Source Path | Notable Items | Complexity |
|---------|-------------|---------------|------------|
| Network Topology Icons | `dwelle/network-topology-icons.excalidrawlib` | Server, Router, Switch, Firewall, Cloud, Laptop, Desktop, Printer | Medium |
| Network Elements | `dwelle/network-elements.excalidrawlib` | Hub, Bridge, Gateway, Access Point, Modem | Simple |

## DevOps & IT

| Library | Source Path | Notable Items | Complexity |
|---------|-------------|---------------|------------|
| Docker/Kubernetes | `psensei/devops-docker-kubernetes.excalidrawlib` | Docker, Kubernetes, Pod, Service, Deployment, Container | Medium |
| IT Logos | `psensei/it-logos.excalidrawlib` | Linux, Windows, Mac, Apache, Nginx, Redis, MongoDB, PostgreSQL | Complex |
| GitHub Icons | `yousifalraheem/github-icons.excalidrawlib` | Pull Request, Issue, Actions, Repository, Branch | Simple |
| DevOps Tools | `ChinoUkaworworx/devops.excalidrawlib` | Jenkins, Terraform, Ansible, GitLab CI, CircleCI | Medium |

## UX & Wireframing

| Library | Source Path | Notable Items | Complexity |
|---------|-------------|---------------|------------|
| Lo-Fi Wireframe Kit | `MarkBlyworker/lo-fi-wireframe-kit.excalidrawlib` | Button, Input, Card, Nav Bar, Modal, Table, Form | Simple |
| Web Wireframe Kit | `nicolo-ribaudo/web-kit.excalidrawlib` | Header, Footer, Sidebar, Hero, Grid, Tabs | Simple |
| Mobile Wireframe Kit | `nicolo-ribaudo/mobile-kit.excalidrawlib` | Phone Frame, Tab Bar, List, Card, Bottom Sheet | Simple |
| HTML Form Inputs | `nicolo-ribaudo/html-inputs.excalidrawlib` | Text Input, Checkbox, Radio, Select, Slider, Toggle | Simple |
| Browser Window | `nicolo-ribaudo/browser-window.excalidrawlib` | Browser chrome, Address bar, Tabs | Simple |

## Data & ML

| Library | Source Path | Notable Items | Complexity |
|---------|-------------|---------------|------------|
| Deep Learning | `psensei/deep-learning.excalidrawlib` | Neural Network, Neuron, Layer, CNN, RNN, Transformer | Medium |
| Data Flow | `francisrstokes/data-flow.excalidrawlib` | Source, Sink, Transform, Filter, Join, Split | Simple |
| Database Icons | `psensei/database-icons.excalidrawlib` | MySQL, PostgreSQL, MongoDB, Redis, Elasticsearch | Medium |

## Diagramming Standards

| Library | Source Path | Notable Items | Complexity |
|---------|-------------|---------------|------------|
| BPMN | `AhmedAlyElGhanwornam/bpmn-2.excalidrawlib` | Start Event, End Event, Task, Gateway, Pool, Lane, Flow | Medium |
| UML Activity | `dwelle/uml-activity.excalidrawlib` | Initial Node, Final Node, Action, Decision, Fork, Join, Merge | Simple |
| UML/ER Shapes | `zhorben/uml-er-shapes.excalidrawlib` | Class, Interface, Entity, Relationship, Inheritance | Simple |
| Sequence Diagram | `Maimunar/sequence-diagrams.excalidrawlib` | Actor, Lifeline, Message, Activation, Fragment | Medium |

## General Purpose

| Library | Source Path | Notable Items | Complexity |
|---------|-------------|---------------|------------|
| Stick Figures | `youritresidence/stick-figures.excalidrawlib` | Walking, Sitting, Pointing, Thinking, Group | Simple |
| Banners & Ribbons | `dbssticky/Excalidraw-banners.excalidrawlib` | Banner, Ribbon, Badge, Tag, Label | Simple |
| 3D Shapes | `psensei/3d-shapes.excalidrawlib` | Cube, Cylinder, Sphere, Cone, Prism | Medium |
| Arrows & Connectors | `drwnio/arrows.excalidrawlib` | Thick Arrow, Curved Arrow, Bidirectional, Dotted | Simple |
| Icons (General) | `lipis/Excalidraw-general-icons.excalidrawlib` | Check, Cross, Star, Heart, Lightning, Lock, Unlock, Gear | Simple |
| Hand Drawn Icons | `maryamalshamiri/hand-drawn-icons.excalidrawlib` | Cloud, Sun, Moon, Tree, House, Car | Simple |

---

## Usage Notes

- **Complexity** indicates how many elements make up typical items: Simple (<10), Medium (10-30), Complex (30+)
- Complex items render best at larger sizes — give them more space in your layout
- Library items come pre-styled; avoid modifying their colors to keep icon recognition
- Source paths may change if libraries are reorganized upstream — if a fetch fails, check the [repo](https://github.com/excalidraw/excalidraw-libraries/tree/main/libraries) for updated paths
- Use `library_helper.py search "keyword"` to find items across cached libraries
