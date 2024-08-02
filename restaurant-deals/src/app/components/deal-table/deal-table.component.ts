import { Component } from '@angular/core';
import { Deal } from '../../models/deal.model';

@Component({
  selector: 'app-deal-table',
  templateUrl: './deal-table.component.html',
  styleUrl: './deal-table.component.css'
})
export class DealTableComponent {
  displayedColumns: string[] = ['restaurantName', 'dealName'];
  data: Deal[] = [
    {dealName: '$7.99 Double Whopper and Small Fries', restaurantId: 1, restaurantName: 'Burger King'},
    {dealName: 'BOGO Double Cheeseburger', restaurantId: 2, restaurantName: 'McDonald\'s'},
    {dealName: '$1.49 Large Fries', restaurantId: 1, restaurantName: 'Burger King'},
    {dealName: '$1.49 Large Onion Rings', restaurantId: 1, restaurantName: 'Burger King'}
  ];

}
