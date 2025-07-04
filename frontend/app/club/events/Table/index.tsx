'use client'

import { Input } from '@/components/ui/input'
import { Button } from '@radix-ui/themes'
import { Table, TableBody, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import EventRow from './row'
import { useEvents } from '../context'

export default function EventsTable() {
  const {
    filteredEvents: events,
    currentPage,
    rowsPerPage,
    totalEvents,
    loading,
    searchQuery,
    setSearchQuery,
    setCurrentPage,
  } = useEvents()

  const indexOfLastEvent = currentPage * rowsPerPage
  const indexOfFirstEvent = indexOfLastEvent - rowsPerPage
  const currentEvents = events.slice(indexOfFirstEvent, indexOfLastEvent)

  const nextPage = () => {
    if (currentPage < Math.ceil(events.length / rowsPerPage)) {
      setCurrentPage(currentPage + 1)
    }
  }

  const prevPage = () => {
    if (currentPage > 1) {
      setCurrentPage(currentPage - 1)
    }
  }

  return (
    <div className="flex flex-col gap-4 p-4">
      <div className="flex flex-col sm:flex-row gap-4 justify-between">
        <div className="relative flex-1">
          <Input
            type="search"
            placeholder="Search events..."
            className="w-full pl-8 bg-muted border-none"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>
      </div>
      <div className="rounded-md border">
        <Table className='overflow-hidden h-auto'>
          <TableHeader>
            <TableRow>
              <TableHead>Event Name</TableHead>
              <TableHead>Date</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Registrations</TableHead>
              <TableHead>Type</TableHead>
              <TableHead>Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {loading ? (
              Array(5)
                .fill(0)
                .map((_, i) => (
                  <TableRow key={i}>
                    <td className="p-4">
                      <div className="h-5 w-35 bg-gray-200 rounded animate-pulse"></div>
                    </td>
                    <td className="p-4">
                      <div className="h-5 w-24 bg-gray-200 rounded animate-pulse"></div>
                    </td>
                    <td className="p-4">
                      <div className="h-5 w-20 bg-gray-200 rounded animate-pulse"></div>
                    </td>
                    <td className="p-4">
                      <div className="h-5 w-32 bg-gray-200 rounded animate-pulse"></div>
                    </td>
                    <td className="p-4">
                      <div className="h-5 w-16 bg-gray-200 rounded animate-pulse"></div>
                    </td>
                    <td className="p-4">
                      <div className="h-5 w-24 bg-gray-200 rounded animate-pulse"></div>
                    </td>
                  </TableRow>
                ))
            ) : currentEvents.length === 0 ? (
              <TableRow>
                <td colSpan={6} className="p-4 text-center text-muted-foreground">
                  No events found matching your search criteria
                </td>
              </TableRow>
            ) : (
              currentEvents.map((event, index) => (
                <EventRow
                  key={event.event_id}
                  index={index}
                />
              ))
            )}
          </TableBody>
        </Table>
      </div>
      <div className="flex items-center justify-between">
        <div className="text-sm text-muted-foreground">
          Showing <strong>{events.length > 0 ? indexOfFirstEvent + 1 : 0}-{Math.min(indexOfLastEvent, totalEvents)}</strong> of{' '}
          <strong>{totalEvents}</strong> events
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" disabled={currentPage === 1 || loading} onClick={prevPage}>
            Previous
          </Button>
          <Button variant="outline" color='gray' className='text-black' disabled={currentPage >= Math.ceil(totalEvents / rowsPerPage) || loading} onClick={nextPage}>
            Next
          </Button>
        </div>
      </div>
    </div>
  )
}