import json
from collections import defaultdict

def merge_data(locations, metadata):
    merged_data = {}
    incomplete_data = []
    
    loc_dict = {item.get('id'): item for item in locations if 'id' in item}
    meta_dict = {item.get('id'): item for item in metadata if 'id' in item}
    
    all_ids = set(loc_dict.keys()) | set(meta_dict.keys())
    
    for id in all_ids:
        merged_data[id] = {}
        
        if id not in loc_dict or id not in meta_dict:
            incomplete_data.append(id)
            
        if id in loc_dict:
            loc_item = loc_dict[id]
            for key, value in loc_item.items():
                merged_data[id][key] = value
        
        if id in meta_dict:
            meta_item = meta_dict[id]
            for key, value in meta_item.items():
                merged_data[id][key] = value
    
    return merged_data, incomplete_data

def analyze_data(merged_data):
    type_counts = defaultdict(int)
    type_ratings = defaultdict(list)
    
    highest_reviews = 0
    highest_review_location = None
    
    valid_points = []
    
    for id, data in merged_data.items():
        if 'latitude' in data and 'longitude' in data and 'type' in data:
            valid_points.append(id)
            
            # Count by type
            type_counts[data['type']] += 1
            
            # Accumulate ratings by type
            if 'rating' in data:
                type_ratings[data['type']].append(data['rating'])
            
            # Track location with highest reviews
            if 'reviews' in data and data['reviews'] > highest_reviews:
                highest_reviews = data['reviews']
                highest_review_location = id
    
    # Calculate average rating per type
    avg_ratings = {}
    for type_name, ratings in type_ratings.items():
        if ratings:
            avg_ratings[type_name] = sum(ratings) / len(ratings)
    
    return {
        'valid_points': valid_points,
        'type_counts': dict(type_counts),
        'avg_ratings': avg_ratings,
        'highest_review_location': highest_review_location,
        'highest_reviews': highest_reviews
    }


def main():
    location_file = open('location.json')
    metadata_file = open('metadata.json')

    locations = json.load(location_file)
    metadata = json.load(metadata_file)

    merged_data, incomplete_data = merge_data(locations, metadata)
    
    if incomplete_data:
        print(f"Found {len(incomplete_data)} locations with incomplete data: {incomplete_data}")
    
    analysis = analyze_data(merged_data)
    
    print("\n===== ANALYSIS RESULTS =====")
    print(f"Total valid points: {len(analysis['valid_points'])}")
    
    print("\nCount per type:")
    for type_name, count in analysis['type_counts'].items():
        print(f"  - {type_name.capitalize()}: {count} locations")
    
    print("\nAverage rating per type:")
    for type_name, avg in analysis['avg_ratings'].items():
        print(f"  - {type_name.capitalize()}: {avg:.1f}/5.0")
    
    print(f"\nLocation with most reviews: {analysis['highest_review_location']}")
    print(f"  - Reviews: {analysis['highest_reviews']}")
    
    print("\nLocations with incomplete data:")
    if incomplete_data:
        for id in incomplete_data:
            missing = []
            if id not in {item.get('id') for item in locations if 'id' in item}:
                missing.append("location coordinates")
            if id not in {item.get('id') for item in metadata if 'id' in item}:
                missing.append("metadata")
            print(f"  - {id}: Missing {', '.join(missing)}")
    else:
        print("  None")
    
    location_file.close()
    metadata_file.close()

if __name__ == "__main__":
    main()