import { NgModule } from '@angular/core';
// import { CommonModule } from '@angular/common';
import { Routes, RouterModule } from '@angular/router';
import { SaltComponent } from './salt/salt.component';
import { SaltminionsComponent } from './saltminions/saltminions.component';
import { ExtComponent } from './ext.component';
const routes: Routes = [
  {
  path: '',
  component: ExtComponent,
  children: [{
    path: '',
    redirectTo: 'minions'
  },
  {
    path: 'cmd',
    component: SaltComponent,
  },
  {
    path: 'minions',
    component: SaltminionsComponent,
  },]
  // {
  //   path: 'd3',
  //   component: D3Component,
  // }, {
  //   path: 'chartjs',
  //   component: ChartjsComponent,
  // }],
}];
@NgModule({
  declarations: [],
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class ExtRoutingModule { }
