# NovaQL

NovaQL is the ultimate advance query language for data + AI era.

## Features
- Piped syntax (like PRQL but better)
- Native vector embeddings & similarity
- Graph traversal & recursion
- Semantic data modeling
- Transpiles to SQL / Polars / DataFusion

## Quick Example
```novaql
from products
| filter embedding <-> [0.1, 0.2, ...] < 0.4
| take 5
