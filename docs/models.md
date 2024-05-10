## Real Estate Project API - Data Models

This document outlines the core data models for the real estate project API. The models leverage a base model (`TimeStampedUUIDModel`) for common fields and relationships.

### TimeStampedUUIDModel (Abstract)

This is an abstract base model used by other models in the API. It provides the following fields:

-   `pkid`: BigAutoField (primary key for internal database management)
-   `id`: UUIDField (unique identifier for the model, automatically generated)
-   `created_at`: DateTimeField (automatically set when the model is created)
-   `updated_at`: DateTimeField (automatically updated whenever the model is saved)

**Relationships:**

-   This is an abstract model and cannot be instantiated directly.

### User

This model extends Django's built-in `AbstractUser` model and defines the following fields:

-   `pkid`: BigAutoField (primary key for internal database management)
-   `id`: UUIDField (unique identifier for the user, automatically generated)
-   `email`: EmailField (unique identifier for login, replaces username)
-   `username`: CharField (optional username, may be blank or null)

**Note:**

-   Authentication uses email instead of username.
-   Required fields for user creation include `username`,  `first_name`, and `last_name`.

### Gender

This model defines a custom field choice for user gender:

-   `MALE`: Male
-   `FEMALE`: Female
-   `OTHER`: Other

### Profile

This model stores user profile information and relates to the `User` model through a OneToOneField relationship.

-   A user can have only one profile.
-   Deleting a user also cascades to delete the associated profile.

The `Profile` model includes the following fields:

-   `user`: OneToOneField (references the user model)
-   `phone_number`: PhoneNumberField (user's phone number with default value)
-   `bio`: TextField (user's short biography)
-   `license`: CharField (optional real estate license number)
-   `profile_photo`: ImageField (user's profile photo with default path)
-   `gender`: CharField (user's gender from the `Gender` choices)
-   `country`: CountryField (user's country with default value)
-   `city`: CharField (user's city)
-   `is_buyer`: BooleanField (indicates if user is looking to buy)
-   `is_seller`: BooleanField (indicates if user is looking to sell)
-   `is_agent`: BooleanField (indicates if user is a real estate agent)
-   `top_agent`: BooleanField (indicates if user is a top agent)
-   `rating`: DecimalField (user's average rating, null by default)
-   `num_reviews`: IntegerField (number of reviews received, null by default)

**Relationships:**

-   A `User` has one and only one `Profile` (OneToOneField).

### Enquiry

This model represents an enquiry submitted by a user through the real estate project website. It inherits from the `TimeStampedUUIDModel` base class.

-   **name (CharField):** User's name (max length 100).
-   **phone_number (PhoneNumberField):** User's phone number with default value.
-   **email (EmailField):** User's email address.
-   **subject (CharField):** Subject of the enquiry (max length 100).
-   **message (TextField):** Content of the enquiry message.

**str method:** Returns a string representation of the enquiry using the user's email address.

**Meta:**

-   `verbose_name_plural`: Enquiries (customizes the plural name in the admin interface).

### Rating

This model represents a user rating for a real estate agent. It leverages the `TimeStampedUUIDModel` base class.

-   **Range (Choices):** Defines rating options:
    
    -   `RATING_1`: Poor (1 star)
    -   `RATING_2`: Fair (2 stars)
    -   `RATING_3`: Good (3 stars)
    -   `RATING_4`: Very Good (4 stars)
    -   `RATING_5`: Excellent (5 stars)
    
-   **rater (ForeignKey):** User who provided the rating (foreign key to the `User` model, allows null values using `SET_NULL` on delete).
-   **agent (ForeignKey):** Agent being rated (foreign key to the `Profile` model, related name `agent_review`, allows null values using `SET_NULL` on delete).
-   **rating (IntegerField):** The rating score (choices from `Range`, default 0).
-   **comment (TextField):** Optional comment from the user about the rating.

**Unique Together:** Enforces a unique combination of `rater` and `agent` to prevent duplicate ratings from the same user for the same agent.

**str method:** Returns a string representation of the rating, including the agent and rating score.

### Property

This model represents a real estate property listing. It inherits from the `TimeStampedUUIDModel` base class.

-   **AdvertType (Choices):** Defines advertisement types:
    
    -   `FOR_SALE`: For Sale
    -   `FOR_RENT`: For Rent
    -   `AUCTION`: Auction
    
-   **PropertyType (Choices):** Defines property types:
    
    -   `HOUSE`: House
    -   `APARTMENT`: Apartment
    -   `OFFICE`: Office
    -   `WAREHOUSE`: Warehouse
    -   `COMMERCIAL`: Commercial
    -   `OTHER`: Other
    
-   **user (ForeignKey):** Agent, seller, or buyer associated with the property (foreign key to the `User` model, related name `agent_buyer`).
-   **title (CharField):** Title of the property (max length 255).
-   **slug (AutoSlugField):** Automatically generated slug based on the title (unique and always updated).
-   **ref_code (CharField):** Unique property reference code (max length 255, may be blank or null).
    
    -   In the `save` method, a random reference code is generated if not provided (`"ES" + 10 random characters`).
    
-   **description (TextField):** Description of the property (optional, default "Default description").
-   **country (CountryField):** Country where the property is located (default "NG").
-   **city (CharField):** City where the property is located (default "Lagos").
-   **postal_code (CharField):** Postal code of the property (default "140").
-   **street_address (CharField):** Street address of the property (default "Street Address").
-   **property_number (IntegerField):** Property number (default 112, minimum value validator ensures it's always positive).
-   **price (DecimalField):** Asking price of the property (default 0.00).
-   **plot_area (DecimalField):** Plot area of the property (default 0.00).
-   **bedrooms (IntegerField):** Number of bedrooms (default 1).
-   **bathrooms (IntegerField):** Number of bathrooms (default 1).
-   **advert_type (CharField):** Advert type (choices from `AdvertType`, default "For Sale").
-   **property_type (CharField):** Property type (choices from `PropertyType`, default "Other").
-   **cover_photo (ImageField):** Main photo of the property (default "/house_sample.jpg", optional).
-   **photo1** to **photo4 (ImageFields):** Additional photos of the property (default "/house_sample.jpg", all optional).
-   **published_status (BooleanField):** Indicates if the property is published (default False).
-   **views (IntegerField):** Total number of views on the property (default 0).

**Objects Managers:**

-   `objects`: Default manager for all properties (including unpublished).
-   `published`: Custom manager to retrieve only published properties.

**str method:** Returns a string representation of the property title.

**Meta:**

-   `verbose_name`: Property (singular)
-   `verbose_name_plural`: Properties (plural)

**save method:**

-   Capitalizes the first letter of each word in the title before saving.
-   Capitalizes the first letter of the description before saving.
-   Generates a unique property reference code (ES + 10 random characters) if not provided.

### PropertyViews

This model tracks the total views for each property listing. It inherits from the `TimeStampedUUIDModel` base class.

-   **ip (CharField):** IP address of the user who viewed the property (max length 255).
-   **property (ForeignKey):** The property being viewed (foreign key to the `Property` model, related name `property_views`).

**str method:** Returns a string representation indicating the total views for a specific property's title.

**Meta:**

-   `verbose_name`: Total views on Property (singular)
-   `verbose_name_plural`: Total Property views (plural)

**Relationships:**

-   A `Property` can have many `PropertyViews` (one-to-many relationship).
-   Deleting a property also cascades to delete all associated property view records.