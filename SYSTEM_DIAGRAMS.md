# 🎨 System Architecture Diagrams

Visual representations of the e-commerce platform with AIRA integration.

---

## 🏗️ High-Level Architecture

```mermaid
graph TB
    subgraph Client
        A[Web Browser]
    end
    
    subgraph Frontend
        B[React App<br/>TypeScript + Tailwind]
        C[React Router]
        D[Axios HTTP Client]
    end
    
    subgraph Backend
        E[Flask Application]
        F[JWT Middleware]
        G[API Routes]
        H[AIRA Handler]
        I[SQLAlchemy ORM]
    end
    
    subgraph Data
        J[(SQLite Database)]
    end
    
    subgraph External
        K[AIRA Platform<br/>Error Monitoring]
    end
    
    A --> B
    B --> C
    C --> D
    D -->|HTTP/JSON| E
    E --> F
    F --> G
    G --> I
    I --> J
    G -.->|On Error| H
    H -->|Webhook| K
```

---

## 🔄 Request Flow with Error Handling

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant B as Backend
    participant D as Database
    participant A as AIRA

    U->>F: Action (e.g., Add to Cart)
    F->>B: HTTP Request + JWT
    B->>B: Validate JWT
    
    alt Valid Request
        B->>D: Query/Update
        D-->>B: Success
        B-->>F: 200 OK + Data
        F-->>U: Update UI
    else Error Occurs
        B->>D: Query/Update
        D-->>B: Error
        B->>B: Log Error
        B->>A: Send Error via Webhook
        A-->>B: Acknowledge
        B-->>F: 4xx/5xx + Error Message
        F-->>U: Show Error
    end
```

---

## 🚨 AIRA Error Capture Flow

```mermaid
graph LR
    A[Exception Occurs] --> B{Error Level?}
    B -->|CRITICAL| C[P0 Severity]
    B -->|ERROR| D[P1 Severity]
    B -->|WARNING| E[P2 Severity]
    B -->|INFO/DEBUG| F[Skip AIRA]
    
    C --> G[Build Payload]
    D --> G
    E --> G
    
    G --> H[Add Context]
    H --> I[Sanitize Data]
    I --> J{Rate Limit OK?}
    
    J -->|Yes| K[Send to Webhook]
    J -->|No| L[Skip Send]
    
    K --> M{Success?}
    M -->|Yes| N[Done]
    M -->|No| O[Retry with Backoff]
    O --> M
```

---

## 🔐 Authentication Flow

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant B as Backend
    participant D as Database

    Note over U,D: Registration Flow
    U->>F: Enter Credentials
    F->>B: POST /api/auth/register
    B->>B: Hash Password
    B->>D: Store User
    D-->>B: User Created
    B-->>F: Success Message
    F-->>U: Redirect to Login

    Note over U,D: Login Flow
    U->>F: Enter Email/Password
    F->>B: POST /api/auth/login
    B->>D: Find User
    D-->>B: User Data
    B->>B: Verify Password
    B->>B: Generate JWT
    B-->>F: JWT Token + User Info
    F->>F: Store Token
    F-->>U: Redirect to Home

    Note over U,D: Protected Request
    U->>F: Access Protected Page
    F->>B: GET /api/cart<br/>Authorization: Bearer TOKEN
    B->>B: Verify JWT
    B->>D: Get Cart Data
    D-->>B: Cart Items
    B-->>F: Cart Data
    F-->>U: Display Cart
```

---

## 🛒 Shopping Cart Flow

```mermaid
graph TD
    A[Browse Books] --> B{User Action}
    B -->|Add to Cart| C[POST /api/cart]
    B -->|View Cart| D[GET /api/cart]
    B -->|Update Quantity| E[PUT /api/cart/:id]
    B -->|Remove Item| F[DELETE /api/cart/:id]
    
    C --> G{Stock Available?}
    G -->|Yes| H[Add to Cart]
    G -->|No| I[Error: Out of Stock]
    I -.->|Log to AIRA| J[P2 Error]
    
    H --> K[Update UI]
    D --> K
    E --> K
    F --> K
    
    K --> L{Checkout?}
    L -->|Yes| M[Create Order]
    L -->|No| A
```

---

## 💳 Order Processing Flow

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant B as Backend
    participant D as Database
    participant P as Payment Gateway
    participant A as AIRA

    U->>F: Click Checkout
    F->>B: POST /api/orders
    B->>D: Get Cart Items
    D-->>B: Cart Data
    
    B->>B: Validate Stock
    
    alt Stock Available
        B->>P: Process Payment
        
        alt Payment Success
            P-->>B: Payment Confirmed
            B->>D: Create Order
            B->>D: Clear Cart
            B->>D: Update Stock
            D-->>B: Order Created
            B-->>F: Order Success
            F-->>U: Show Confirmation
        else Payment Failed
            P-->>B: Payment Error
            B->>A: Log P1 Error
            B-->>F: Payment Failed
            F-->>U: Show Error
        end
    else Insufficient Stock
        B->>A: Log P2 Error
        B-->>F: Stock Error
        F-->>U: Show Error
    end
```

---

## 📊 Database Schema Relationships

```mermaid
erDiagram
    USERS ||--o{ CART : has
    USERS ||--o{ ORDERS : places
    BOOKS ||--o{ CART : contains
    BOOKS ||--o{ ORDER_ITEMS : includes
    ORDERS ||--|{ ORDER_ITEMS : contains

    USERS {
        int id PK
        string email UK
        string username UK
        string password_hash
        datetime created_at
    }

    BOOKS {
        int id PK
        string title
        string author
        decimal price
        int stock
        text description
        string cover_image
        string isbn UK
        datetime created_at
    }

    CART {
        int id PK
        int user_id FK
        int book_id FK
        int quantity
        datetime created_at
    }

    ORDERS {
        int id PK
        int user_id FK
        decimal total_amount
        string status
        datetime created_at
    }

    ORDER_ITEMS {
        int id PK
        int order_id FK
        int book_id FK
        int quantity
        decimal price
    }
```

---

## 🧪 Error Testing Scenarios

```mermaid
graph TB
    A[Test Endpoints] --> B[P0: Database Error]
    A --> C[P1: Payment Error]
    A --> D[P1: Auth Error]
    A --> E[P2: Stock Error]
    A --> F[P2: Invalid ID]
    A --> G[P2: Validation Error]
    
    B --> H[/api/test/error/database]
    C --> I[/api/test/error/payment]
    D --> J[/api/test/error/auth]
    E --> K[/api/test/error/stock]
    F --> L[/api/books/99999]
    G --> M[/api/test/error/validation]
    
    H -.->|Logs to| N[AIRA Dashboard]
    I -.->|Logs to| N
    J -.->|Logs to| N
    K -.->|Logs to| N
    L -.->|Logs to| N
    M -.->|Logs to| N
    
    N --> O[View Errors]
    N --> P[Analyze Context]
    N --> Q[Review Stack Traces]
```

---

## 🔄 AIRA Handler Internal Flow

```mermaid
graph TD
    A[Error Occurs in Flask] --> B[Python Logging System]
    B --> C{Log Level >= ERROR?}
    C -->|No| D[Skip AIRA]
    C -->|Yes| E[AIRA Handler.emit]
    
    E --> F[Extract Context]
    F --> G[Get User Info]
    F --> H[Get Request Info]
    F --> I[Get Error Info]
    
    G --> J[Build Payload]
    H --> J
    I --> J
    
    J --> K[Sanitize Sensitive Data]
    K --> L{Rate Limit Check}
    
    L -->|Exceeded| M[Skip Send]
    L -->|OK| N[Async HTTP Request]
    
    N --> O{Response OK?}
    O -->|Yes| P[Success]
    O -->|No| Q{Retry < Max?}
    
    Q -->|Yes| R[Exponential Backoff]
    R --> N
    Q -->|No| S[Log Failure Locally]
    
    M --> T[Continue App]
    P --> T
    S --> T
```

---

## 🎯 Component Interaction Map

```mermaid
graph TB
    subgraph Frontend Components
        A[App.tsx]
        B[Navbar]
        C[Home Page]
        D[Book Detail]
        E[Cart Page]
        F[Checkout]
        G[Login/Register]
        H[Order History]
    end
    
    subgraph Services
        I[API Service]
        J[Auth Service]
    end
    
    subgraph Backend Routes
        K[Auth Routes]
        L[Book Routes]
        M[Cart Routes]
        N[Order Routes]
        O[Test Routes]
    end
    
    A --> B
    A --> C
    A --> D
    A --> E
    A --> F
    A --> G
    A --> H
    
    C --> I
    D --> I
    E --> I
    F --> I
    G --> J
    H --> I
    
    I --> K
    I --> L
    I --> M
    I --> N
    J --> K
    
    O -.->|Testing| I
```

---

## 📱 Frontend State Management

```mermaid
stateDiagram-v2
    [*] --> Unauthenticated
    
    Unauthenticated --> Authenticated: Login Success
    Authenticated --> Unauthenticated: Logout
    
    state Authenticated {
        [*] --> Browsing
        Browsing --> ViewingBook: Select Book
        ViewingBook --> Browsing: Back
        ViewingBook --> CartUpdated: Add to Cart
        
        CartUpdated --> ViewingCart: View Cart
        ViewingCart --> Browsing: Continue Shopping
        ViewingCart --> Checkout: Proceed
        
        Checkout --> OrderPlaced: Payment Success
        Checkout --> CartUpdated: Payment Failed
        
        OrderPlaced --> ViewingOrders: View Orders
        ViewingOrders --> Browsing: Continue Shopping
    }
```

---

## 🔒 Security Layers

```mermaid
graph TB
    A[User Request] --> B{CORS Check}
    B -->|Fail| C[403 Forbidden]
    B -->|Pass| D{JWT Valid?}
    
    D -->|No| E[401 Unauthorized]
    D -->|Yes| F{Rate Limit OK?}
    
    F -->|No| G[429 Too Many Requests]
    F -->|Yes| H{Input Valid?}
    
    H -->|No| I[400 Bad Request]
    H -->|Yes| J[Process Request]
    
    J --> K{Error Occurs?}
    K -->|Yes| L[Log to AIRA]
    K -->|No| M[Return Success]
    
    L --> N[Sanitize Data]
    N --> O[Send to Webhook]
    O --> P[Return Error Response]
```

---

## 📈 Performance Considerations

```mermaid
graph LR
    A[Request] --> B[Flask Processing]
    B --> C[Database Query]
    C --> D[Response]
    
    B -.->|On Error| E[AIRA Handler]
    E -.->|Async| F[Webhook Call]
    
    style F fill:#90EE90
    
    Note1[Non-blocking<br/>Async call]
    Note2[Main request<br/>not delayed]
    
    F -.-> Note1
    D -.-> Note2
```

---

## 🎓 Learning Path

```mermaid
graph TD
    A[Start] --> B[Understand Architecture]
    B --> C[Setup Backend]
    C --> D[Implement AIRA Handler]
    D --> E[Test AIRA Integration]
    E --> F[Build API Routes]
    F --> G[Setup Frontend]
    G --> H[Connect Frontend-Backend]
    H --> I[Test Error Scenarios]
    I --> J[Review AIRA Dashboard]
    J --> K[Optimize & Document]
    K --> L[Complete!]
    
    style D fill:#FFD700
    style E fill:#FFD700
    style I fill:#FFD700
    style J fill:#FFD700
```

---

## 🚀 Deployment Architecture (Future)

```mermaid
graph TB
    subgraph Production
        A[Load Balancer]
        B[Flask App 1]
        C[Flask App 2]
        D[PostgreSQL]
        E[Redis Cache]
    end
    
    subgraph Monitoring
        F[AIRA Platform]
        G[Application Logs]
    end
    
    A --> B
    A --> C
    B --> D
    C --> D
    B --> E
    C --> E
    
    B -.->|Errors| F
    C -.->|Errors| F
    B -.->|Logs| G
    C -.->|Logs| G
```

---

These diagrams provide visual representations of:
- System architecture
- Request flows
- Error handling
- Authentication
- Database relationships
- Component interactions
- Security layers
- Performance considerations

Use these diagrams to understand the system before implementation!