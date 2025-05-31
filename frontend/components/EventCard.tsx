'use client'
import Link from 'next/link';
import { Calendar, MapPin } from 'lucide-react';
import { Badge, Button } from '@radix-ui/themes';
import { Card, CardContent } from '@/components/ui/card';
import { motion } from 'framer-motion';
import ImageComponent from '@/components/ImageComponent';
import { Event } from './types/EventCardTypes';

export default function EventCard(item: Event) {
  return (
    <motion.div
      key={item.event_id}
      className="h-full"
      initial={{ opacity: 0, scale: 0.95, filter: 'blur(10px)' }}
      animate={{ opacity: 1, scale: 1, filter: 'blur(0px)', transition: { duration: 0.3 } }}
      exit={{ opacity: 0, scale: 0.95, filter: 'blur(10px)', transition: { duration: 0.2 } }}
      whileHover={{ y: -8 }}
      layout
    >
      <Link href={`/event/${item.event_id}`}>
        <Card className="overflow-hidden hover:shadow-xl transition-shadow rounded-2xl border-0">
          {/* Background image */}
          <div className="absolute inset-0 rounded-2xl overflow-hidden">
            <ImageComponent imageFile={item.imageUrl} alt={item.title} className="object-cover w-full h-full" />
          </div>
          {/* image placeholder */}
          <div className="relative h-44 w-full" />
          <CardContent className="
            h-52
            flex 
            flex-col 
            justify-center
            p-4
            py-6 
            bg-black/30 
            backdrop-blur-md 
            rounded-2xl 
            relative 
            z-10
          ">
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <h5 className="font-semibold line-clamp-1 m-0 text-white text-lg">{item.title}</h5>
                {item.is_paid ? (
                  <Badge color="gray" highContrast variant="solid">
                    Rs. {item.price}
                  </Badge>
                ) : (
                  <Badge variant="outline" color="gray">Free</Badge>
                )}
              </div>
              <div className="space-y-1 text-sm flex flex-col gap-2">
                <div className="flex items-center">
                  <Calendar className="mr-2 h-4 w-4 text-white" />
                  <span className="text-white">
                    {new Date(item.event_date).toLocaleDateString()} —{' '}
                    {new Date(item.event_date).toLocaleTimeString()}
                  </span>
                </div>
                <div className="flex items-center">
                  <MapPin className="mr-2 h-4 w-4 text-white" />
                  <span className="line-clamp-1 text-white">{item.location}</span>
                </div>
              </div>
            </div>
            <Button
              color="gray"
              variant="solid"
              highContrast
              className="mt-3 w-full"
            >
              View Details
            </Button>
          </CardContent>
        </Card>
      </Link>
    </motion.div>
  );
}