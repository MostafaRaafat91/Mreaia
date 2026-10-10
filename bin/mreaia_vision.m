#import <Foundation/Foundation.h>
#import <Vision/Vision.h>
#import <AppKit/AppKit.h>
#import <CoreImage/CoreImage.h>

int main(int argc, const char * argv[]) {
    @autoreleasepool {
        if (argc < 2) {
            printf("{}\n");
            return 1;
        }
        NSString *path = [NSString stringWithUTF8String:argv[1]];
        NSImage *image = [[NSImage alloc] initWithContentsOfFile:path];
        if (!image) {
            printf("{\"faces_count\":0,\"faces\":[],\"detected_objects\":[]}\n");
            return 0;
        }
        NSData *tiffData = [image TIFFRepresentation];
        CIImage *ciImage = [CIImage imageWithData:tiffData];
        if (!ciImage) {
            printf("{\"faces_count\":0,\"faces\":[],\"detected_objects\":[]}\n");
            return 0;
        }

        VNImageRequestHandler *handler = [[VNImageRequestHandler alloc] initWithCIImage:ciImage options:@{}];
        VNClassifyImageRequest *classifyReq = [[VNClassifyImageRequest alloc] init];
        VNDetectFaceLandmarksRequest *faceReq = [[VNDetectFaceLandmarksRequest alloc] init];

        NSError *error = nil;
        [handler performRequests:@[classifyReq, faceReq] error:&error];

        // 1. Process Objects & Scene Classes
        NSMutableArray *objects = [NSMutableArray array];
        for (VNClassificationObservation *obs in classifyReq.results) {
            if (obs.confidence > 0.20) {
                [objects addObject:@{
                    @"name": obs.identifier,
                    @"confidence": @(round(obs.confidence * 100.0) / 100.0)
                }];
                if (objects.count >= 8) break;
            }
        }

        // 2. Process Faces & Landmark-based Emotion Analysis
        NSMutableArray *faces = [NSMutableArray array];
        for (VNFaceObservation *face in faceReq.results) {
            NSString *emotion = @"neutral / composed";
            double emotionConfidence = 0.85;

            VNFaceLandmarks2D *landmarks = face.landmarks;
            if (landmarks.outerLips && landmarks.outerLips.pointCount >= 6) {
                const CGPoint *points = landmarks.outerLips.normalizedPoints;
                NSUInteger count = landmarks.outerLips.pointCount;
                
                // Estimate smile and mouth openness
                CGPoint leftCorner = points[0];
                CGPoint rightCorner = points[count / 2];
                CGPoint topLip = points[count / 4];
                CGPoint bottomLip = points[(3 * count) / 4];
                
                CGFloat cornerHeightAvg = (leftCorner.y + rightCorner.y) / 2.0;
                CGFloat mouthOpening = fabs(topLip.y - bottomLip.y);
                CGFloat smileLift = cornerHeightAvg - bottomLip.y;

                if (smileLift > 0.025) {
                    emotion = @"smiling / happy / confident";
                    emotionConfidence = 0.91;
                } else if (mouthOpening > 0.055) {
                    emotion = @"expressive / passionate / speaking";
                    emotionConfidence = 0.88;
                } else if (cornerHeightAvg < bottomLip.y - 0.015) {
                    emotion = @"serious / stern / concerned";
                    emotionConfidence = 0.84;
                }
            }

            [faces addObject:@{
                @"confidence": @(round(face.confidence * 100.0) / 100.0),
                @"primary_emotion": emotion,
                @"emotion_confidence": @(emotionConfidence),
                @"bounding_box": @{
                    @"x": @(round(face.boundingBox.origin.x * 1000.0) / 1000.0),
                    @"y": @(round(face.boundingBox.origin.y * 1000.0) / 1000.0),
                    @"w": @(round(face.boundingBox.size.width * 1000.0) / 1000.0),
                    @"h": @(round(face.boundingBox.size.height * 1000.0) / 1000.0)
                }
            }];
        }

        NSDictionary *output = @{
            @"faces_count": @(faces.count),
            @"faces": faces,
            @"detected_objects": objects
        };

        NSData *jsonData = [NSJSONSerialization dataWithJSONObject:output options:0 error:nil];
        NSString *jsonStr = [[NSString alloc] initWithData:jsonData encoding:NSUTF8StringEncoding];
        printf("%s\n", [jsonStr UTF8String]);
    }
    return 0;
}
